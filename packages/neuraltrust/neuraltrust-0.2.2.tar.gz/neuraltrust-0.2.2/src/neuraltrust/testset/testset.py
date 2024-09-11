from typing import Any, List, Optional, Dict
from dataclasses import dataclass, field
from ..services.api_service import NeuralTrustApiService

@dataclass
class TestsetRow:
    query: Optional[str] = None
    context: Optional[List[str]] = None
    response: Optional[str] = None
    expected_response: Optional[str] = None
    conversation_history: Optional[List[Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Testset:
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    rows: List[TestsetRow] = field(default_factory=list)

    @staticmethod
    def create(
        id: str,
        testset_id: str,
        rows: List[TestsetRow] = None,
    ):
        """
        Creates a new testset with the specified properties.
        Parameters:
        - id (str): The ID of the testset. This is a required field.
        - rows (List[TestsetRow]): Optional list of TestsetRow objects to be added to the testset.

        Returns:
        The newly created testset object

        Raises:
        - Exception: If the testset could not be created due to an error like invalid parameters, database errors, etc.
        """
        testset_data = []

        if rows:
            for row in rows:
                row_data = row.__dict__.copy()  # Create a copy of the TestsetRow attributes
                row_data["testsetId"] = testset_id  # Add testset_id to each row
                row_data["evaluationSetId"] = id
                row_data["expectedResponse"] = row.expected_response
                row_data["conversationHistory"] = row.conversation_history
                row_data["type"] = row.metadata["question_type"]
                del row_data["expected_response"]
                del row_data["conversation_history"]
                # Remove None values from the row data
                row_data = {k: v for k, v in row_data.items() if v is not None}
                testset_data.append(row_data)

        try:
            NeuralTrustApiService.create_testset(testset_data)
        except Exception as e:
            raise

        testset = Testset(id=id)
        return testset

    @staticmethod
    def update(
        testset_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        language_model_id: Optional[str] = None,
        prompt_template: Optional[Any] = None,
        rows: Optional[List[TestsetRow]] = None,
    ):
        """
        Updates an existing testset with the specified properties.
        
        Parameters:
        - testset_id (str): The ID of the testset to update.
        - name (Optional[str]): An optional new name for the testset.
        - description (Optional[str]): An optional new description for the testset.
        - language_model_id (Optional[str]): An optional new identifier for the language model associated with this testset.
        - prompt_template (Optional[Any]): An optional new template for prompts used in this testset.
        - rows (Optional[List[TestsetRow]]): Optional new rows to replace the existing rows in the testset.

        Returns:
        The updated testset object.

        Raises:
        - Exception: If the testset could not be updated due to an error like invalid parameters, database errors, etc.
        """
        update_data = {
            "name": name,
            "description": description,
            "languageModelId": language_model_id,
            "promptTemplate": prompt_template,
            "testsetRows": rows,
        }
        # Remove keys where the value is None
        update_data = {k: v for k, v in update_data.items() if v is not None}

        try:
            updated_testset_data = NeuralTrustApiService.update_testset(testset_id, update_data)
        except Exception as e:
            raise

        updated_testset = Testset(
            id=updated_testset_data["id"],
            source=updated_testset_data["source"],
            name=updated_testset_data["name"],
            description=updated_testset_data["description"],
            language_model_id=updated_testset_data["languageModelId"],
            prompt_template=updated_testset_data["promptTemplate"],
        )
        return updated_testset

    @staticmethod
    def fetch_testset_rows(testset_id: str, number_of_rows: Optional[int] = None):
        """
        Fetches the rows of a testset.

        Parameters:
        - testset_id (str): The ID of the testset to fetch rows.
        """
        return NeuralTrustApiService.fetch_testset_rows(testset_id, number_of_rows)

    @staticmethod
    def testset_link(testset_id: str):
        return f"https://app.neuraltrust.ai"