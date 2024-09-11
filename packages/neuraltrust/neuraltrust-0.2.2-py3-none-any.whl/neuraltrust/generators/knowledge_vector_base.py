from typing import Dict, Optional, Sequence, List
import logging
import uuid
import numpy as np
from sklearn.cluster import HDBSCAN
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
import pandas as pd
from sklearn.decomposition import PCA
import os

from .base_knowledge_base import BaseKnowledgeBase
from ..llm.client import ChatMessage, LLMClient, get_judge_client
from ..llm.embeddings import get_default_embedding
from ..llm.embeddings.base import BaseEmbedding
from ..errors.exceptions import ImportError
from ..utils.language_detection import detect_lang
from datetime import datetime

try:
    import umap
except ImportError as err:
    raise ImportError(missing_package="umap") from err

logger = logging.getLogger("neuraltrust.generators")

LANGDETECT_MAX_TEXT_LENGTH = 300
LANGDETECT_DOCUMENTS = 10

TOPIC_SUMMARIZATION_PROMPT = """Your task is to define the topic which best represents a set of documents.

Your are given below a list of documents and you must extract the topic best representing ALL contents.
- The topic name should be between 1 to 5 words
- Provide the topic in this language: {language}

Make sure to only return the topic name between quotes, and nothing else.

For example, given these documents:

<documents>
Camembert is a moist, soft, creamy, surface-ripened cow's milk cheese.
----------
Bleu d'Auvergne is a French blue cheese, named for its place of origin in the Auvergne region.
----------
Roquefort is a sheep milk cheese from the south of France.
</documents>

The topic is:
"French Cheese"

Now it's your turn. Here is the list of documents:

<documents>
{topics_elements}
</documents>

The topic is:
"""


class Document:
    """A class to wrap the elements of the knowledge base into a unified format."""

    def __init__(
        self, document: Dict[str, str]
    ):
        self.content = document.get('content', '')
        self.filename = document.get('filename', '')
        self.id = document.get('id', str(uuid.uuid4()))
        self.embeddings = document.get('contentVector', None)
        self.reduced_embeddings = None
        self.topic_id = None


class KnowledgeVectorBase(BaseKnowledgeBase):
    """
    A class to handle the knowledge base and the associated vector store using Azure AI Search.

    Parameters
    ----------
    search_service_name: str
        The name of your Azure AI Search service.
    index_name: str
        The name of the index in your Azure AI Search service.
    credential: AzureKeyCredential
        The credential for authenticating with Azure AI Search.
    seed: int, optional
        The seed to use for random number generation.
    llm_client: LLMClient, optional
        The LLM client to use for question generation. If not specified, a default openai client will be used.
    embedding_model: BaseEmbedding, optional
        The embedding model to use for the knowledge base. By default, we use the default embedding model.
    min_topic_size: int, optional
        The minimum number of documents to form a topic inside the knowledge base.
    allow_empty_index: bool, optional
        Whether to allow the index to be empty when initializing the KnowledgeVectorBase.
    """

    def __init__(
        self,
        search_service_name: str,
        index_name: str,
        api_key: str,
        seed: int = None,
        llm_client: Optional[LLMClient] = None,
        embedding_model: Optional[BaseEmbedding] = None,
        min_topic_size: Optional[int] = 2,
        allow_empty_index: bool = False
    ) -> None:
        self.search_client = SearchClient(
            endpoint=f"https://{search_service_name}.search.windows.net/",
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )

        self._rng = np.random.default_rng(seed=seed)
        self._llm_client = llm_client or get_judge_client()
        self._embedding_model = embedding_model or get_default_embedding()

        self._documents = self._load_documents()
        if len(self._documents) == 0 and not allow_empty_index:
            raise ValueError("Cannot generate a Knowledge Base from empty index.")

        # Estimate the minimum number of documents to form a topic
        if min_topic_size is not None:
            self._min_topic_size = min_topic_size
        elif len(self._documents) > 0:
            self._min_topic_size = round(2 + np.log(len(self._documents)))
        else:
            self._min_topic_size = 2  # Default value when documents are empty

        self._topics_inst = None
        self._reduced_embeddings_inst = None

        # Detect language of the documents
        document_languages = [
            detect_lang(doc.content[:LANGDETECT_MAX_TEXT_LENGTH])
            for doc in self._rng.choice(self._documents, size=min(LANGDETECT_DOCUMENTS, len(self._documents)))
        ]
        languages, occurrences = np.unique(
            ["en" if (lang is None or pd.isna(lang) or lang == "unknown") else lang for lang in document_languages],
            return_counts=True
        )
        
        # Handle the case when occurrences is empty
        if len(occurrences) > 0:
            self._language = languages[np.argmax(occurrences)]
        else:
            self._language = "en"  # Default to English if no language is detected
        

    def _load_documents(self):
        # Load all documents from Azure AI Search index
        results = list(self.search_client.search("*", top=1000))
        documents = [Document(doc) for doc in results]
        return documents

    @property
    def language(self):
        return self._language
    
    @property
    def _embeddings(self):
        embeddings = np.array([doc.embeddings for doc in self._documents if doc.embeddings is not None])
        if len(embeddings) == 0:
            logger.warning("No embeddings found in documents")
            return None
        return embeddings

    @property
    def _reduced_embeddings(self):
        if self._reduced_embeddings_inst is None:
            embeddings = self._embeddings
            if embeddings is None or len(embeddings) == 0:
                logger.warning("Cannot calculate UMAP projection: no embeddings available")
                return None
            logger.debug("Calculating UMAP projection")
            
            n_samples = embeddings.shape[0]
            n_components = min(2, n_samples - 1)  # Ensure n_components is less than n_samples
            
            reducer = umap.UMAP(
                n_neighbors=min(50, n_samples - 1),  # Ensure n_neighbors is less than n_samples
                min_dist=0.5,
                n_components=n_components,
                random_state=1234,
                n_jobs=1,
            )
            
            try:
                self._reduced_embeddings_inst = reducer.fit_transform(embeddings)
            except ValueError as e:
                logger.warning(f"UMAP projection failed: {str(e)}")
                # Fallback to PCA if UMAP fails
                pca = PCA(n_components=n_components)
                self._reduced_embeddings_inst = pca.fit_transform(embeddings)
            
            for doc, emb in zip(self._documents, self._reduced_embeddings_inst):
                doc.reduced_embeddings = emb
        return self._reduced_embeddings_inst

    @property
    def topics(self):
        if self._topics_inst is None:
            self._topics_inst = self._find_topics()
        return self._topics_inst

    def _find_topics(self):
        logger.info("Finding topics in the knowledge base.")
        reduced_embeddings = self._reduced_embeddings
        if reduced_embeddings is None or len(reduced_embeddings) == 0:
            logger.warning("Cannot find topics: no reduced embeddings available")
            return {"Others": "Others"}
        hdbscan = HDBSCAN(
            min_cluster_size=self._min_topic_size,
            min_samples=5,
            metric="euclidean",
            cluster_selection_epsilon=0.0,
        )
        clustering = hdbscan.fit(reduced_embeddings)
        
        for i, doc in enumerate(self._documents):
            doc.topic_id = clustering.labels_[i]

        topics_ids = set(clustering.labels_)
        topics = {
            idx: self._get_topic_name([doc for doc in self._documents if doc.topic_id == idx])
            for idx in topics_ids
            if idx != -1
        }
        topics[-1] = "Others"

        return topics

    def _get_topic_name(self, topic_documents):
        self._rng.shuffle(topic_documents)
        topics_str = "\n\n".join(["----------" + doc.content[:500] for doc in topic_documents[:10]])

        # prevent context window overflow
        topics_str = topics_str[: 3 * 8192]
        prompt = TOPIC_SUMMARIZATION_PROMPT.format(language=self._language, topics_elements=topics_str)

        raw_output = self._llm_client.complete([ChatMessage(role="user", content=prompt)], temperature=0.0).content

        return raw_output.strip().strip('"')

    def get_random_document(self):
        return self._rng.choice(self._documents)

    def get_neighbors(self, seed_document: Document, n_neighbors: int = 4, similarity_threshold: float = 0.2):
        seed_embedding = seed_document.embeddings
        vector_query = VectorizedQuery(vector=seed_embedding, k_nearest_neighbors=n_neighbors, fields="contentVector")
        results = list(self.search_client.search(
            search_text="",
            vector_queries=[vector_query],
            select="id,content,contentVector",
            top=n_neighbors
        ))
        return [Document(doc) for doc in results if doc['@search.score'] > similarity_threshold]

    def similarity_search_with_score(self, query: str, k: int) -> Sequence:
        query_emb = self._embedding_model.embed(query)
        vector_query = VectorizedQuery(vector=query_emb, k_nearest_neighbors=k, fields="contentVector")
        results = list(self.search_client.search(
            search_text="",
            vector_queries=[vector_query],
            select="id,content,contentVector",
            top=k
        ))
        return [(Document(doc), doc['@search.score']) for doc in results]

    def __len__(self):
        return len(self._documents)

    def __getitem__(self, doc_id: str):
        return next((doc for doc in self._documents if doc.id == doc_id), None)

    @classmethod
    def from_pdf(cls, path: str, search_service_name: str, index_name: str, api_key: str, **kwargs):
        """
        Create a KnowledgeVectorBase from a PDF file or a directory containing PDF files.

        Parameters
        ----------
        path : str
            Path to the PDF file or directory containing PDF files.
        search_service_name : str
            The name of your Azure AI Search service.
        index_name : str
            The name of the index in your Azure AI Search service.
        api_key : str
            The API key for authenticating with Azure AI Search.
        **kwargs :
            Additional keyword arguments to pass to the KnowledgeVectorBase constructor.

        Returns
        -------
        KnowledgeVectorBase
            An instance of KnowledgeVectorBase with the PDF content embedded and stored in Azure AI Search.
        """
        # Initialize the KnowledgeVectorBase with allow_empty_index=True
        kb = cls(search_service_name, index_name, api_key, allow_empty_index=True, **kwargs)

        pdf_files = []
        if os.path.isdir(path):
            # If path is a directory, get all PDF files
            for root, _, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        elif os.path.isfile(path) and path.lower().endswith('.pdf'):
            # If path is a single PDF file
            pdf_files.append(path)
        else:
            raise ValueError("The provided path is neither a PDF file nor a directory containing PDF files.")

        for pdf_path in pdf_files:
            # Extract text from PDF
            text_chunks = kb._extract_text_from_pdf(pdf_path)

            # Compute embeddings using Azure OpenAI
            embeddings = kb._compute_embeddings(text_chunks)

            # Write to vector store
            kb._write_to_vector_store(text_chunks, embeddings, pdf_path)

        # Reload documents after writing to the vector store
        kb._documents = kb._load_documents()

        return kb

    def _extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        """
        Extract text from a PDF file and split it into chunks.

        Parameters
        ----------
        pdf_path : str
            Path to the PDF file.

        Returns
        -------
        List[str]
            A list of text chunks extracted from the PDF.
        """
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("PyPDF2 is required to extract text from PDF files. Install it using 'pip install PyPDF2'.")

        text_chunks = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                # Split text into chunks (you may want to implement a more sophisticated chunking method)
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                text_chunks.extend(chunks)

        return text_chunks

    def _compute_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Compute embeddings for text chunks using Azure OpenAI.

        Parameters
        ----------
        text_chunks : List[str]
            List of text chunks to compute embeddings for.

        Returns
        -------
        List[List[float]]
            A list of embeddings for each text chunk.
        """
        
        embeddings = []
        for chunk in text_chunks:
            _embeddings_inst = np.array(self._embedding_model.embed(texts=[chunk]))
            embeddings.append(_embeddings_inst)

        return embeddings

    def _write_to_vector_store(self, text_chunks: List[str], embeddings: List[List[float]], pdf_path: str):
        """
        Write text chunks and their embeddings to the Azure AI Search index.

        Parameters
        ----------
        text_chunks : List[str]
            List of text chunks to be stored.
        embeddings : List[List[float]]
            List of embeddings corresponding to the text chunks.
        pdf_path : str
            Path to the original PDF file.
        """
        documents = []
        for i, (text, embedding) in enumerate(zip(text_chunks, embeddings)):
            doc = {
                "id": f"chunk_{i}",
                "content": text,
                "filepath": pdf_path,
                "title": pdf_path.split("/")[-1],
                "url": "",
                "contentVector": embedding.flatten().tolist()
            }
            documents.append(doc)

        # Upload documents in batches
        batch_size = 1000
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            self.search_client.upload_documents(documents=batch)

        print(f"Uploaded {len(documents)} documents to Azure AI Search index.")

    @classmethod
    def from_text(cls, file_path: str, search_service_name: str, index_name: str, api_key: str, **kwargs):
        """
        Create a KnowledgeVectorBase from a text file.

        Parameters
        ----------
        file_path : str
            The path to the text file to be processed and stored.
        search_service_name : str
            The name of your Azure AI Search service.
        index_name : str
            The name of the index in your Azure AI Search service.
        api_key : str
            The API key for authenticating with Azure AI Search.
        **kwargs :
            Additional keyword arguments to pass to the KnowledgeVectorBase constructor.

        Returns
        -------
        KnowledgeVectorBase
            An instance of KnowledgeVectorBase with the text file content embedded and stored in Azure AI Search.
        """
        # Initialize the KnowledgeVectorBase with allow_empty_index=True
        kb = cls(search_service_name, index_name, api_key, allow_empty_index=True, **kwargs)

        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split text into chunks
        text_chunks = kb._split_text(text)
        # Compute embeddings
        embeddings = kb._compute_embeddings(text_chunks)

        # Write to vector store
        kb._write_to_vector_store(text_chunks, embeddings, file_path)

        # Reload documents after writing to the vector store
        kb._documents = kb._load_documents()

        return kb

    def _split_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Split the input text into chunks.

        Parameters
        ----------
        text : str
            The input text to be split.
        chunk_size : int, optional
            The maximum size of each chunk. Default is 1000 characters.

        Returns
        -------
        List[str]
            A list of text chunks.
        """
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]