import typing
import os
import uuid
import datetime as dt
from importlib.metadata import version
from concurrent.futures import ThreadPoolExecutor

from .api_client import (
    NeuralTrustApi,
    TraceResponse,
    TraceTask,
    User,
    Metadata
)

OMIT = typing.cast(typing.Any, ...)

DEFAULT_BASE_URL = "https://api.neuraltrust.ai"

class NeuralTrust:
    base_client: NeuralTrustApi
    executor: ThreadPoolExecutor

    def __init__(
        self,
        api_key: typing.Union[str, None] = None,
        base_url: typing.Union[str, None] = None,
        sdk_version: typing.Union[str, None] = 'v1',
        timeout: typing.Union[float, None] = None,
        max_workers: typing.Union[int, None] = 5,
    ) -> None:
        
        if not api_key:
            api_key = os.environ.get("NEURALTRUST_API_KEY")
        
        if not base_url:
            base_url = os.environ.get("NEURALTRUST_BASE_URL") or DEFAULT_BASE_URL
        
        self.trace_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.base_client = NeuralTrustApi(
            api_key=api_key, base_url=f"{base_url}/{sdk_version}", timeout=timeout
        )
        # set base URL
        if base_url:
            self.base_client._client_wrapper._base_url = f"{base_url}/{sdk_version}"
    @property
    def api_key(self) -> typing.Union[str, None]:
        """Property getter for api_key."""
        return self.base_client._client_wrapper.api_key

    @api_key.setter
    def api_key(self, value: typing.Union[str, None]) -> None:
        """Property setter for api_key."""
        self.api_key = value
        if value is not None:
            self.base_client._client_wrapper.api_key = value

    @property
    def base_url(self) -> typing.Union[str, None]:
        """Property getter for base_url."""
        return self.base_client._client_wrapper._base_url

    @base_url.setter
    def base_url(self, value: typing.Union[str, None]) -> None:
        """Property setter for base_url."""
        if value is not None:
            self.base_client._client_wrapper._base_url = value

    def trace(self, conversation_id: str = None, session_id: str = None, channel_id: str = None, user: User = None, metadata: Metadata = None, custom: dict = None):
        return Trace(client=self, conversation_id=conversation_id, session_id=session_id, channel_id=channel_id, user=user, metadata=metadata, custom=custom)
    
    def _trace(
        self,
        *,
        type: typing.Optional[str] = OMIT,
        task: typing.Optional[TraceTask] = OMIT,
        input: typing.Optional[str] = OMIT,
        output: typing.Optional[str] = OMIT,
        user: typing.Optional[User] = OMIT,
        metadata: typing.Optional[Metadata] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        channel_id: typing.Optional[str] = OMIT,
        conversation_id: typing.Optional[str] = OMIT,
        interaction_id: typing.Optional[str] = OMIT,
        start_timestamp: typing.Optional[int] = OMIT,
        end_timestamp: typing.Optional[int] = OMIT,
        custom: typing.Optional[str] = OMIT
    ) -> TraceResponse:
        return self.trace_executor.submit(
            self.base_client.trace,
            type=type,
            task=task,
            input=input,
            output=output,
            user=user,
            metadata=metadata,
            session_id=session_id,
            channel_id=channel_id,
            conversation_id=conversation_id,
            interaction_id=interaction_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            custom=custom
        )

class Trace:
    def __init__(self, client, conversation_id: str = None, channel_id: str = None, session_id: str = None, user: typing.Optional[User] = None, metadata: typing.Optional[Metadata] = None, custom: typing.Optional[dict] = None):
        self.client = client
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.session_id = session_id
        self.interaction_id = str(uuid.uuid4())
        self.channel_id = channel_id
        self.user = user
        self.metadata = metadata
        self.custom = custom
        self.start_timestamp = None
        self.end_timestamp = None
        self.input = None
        self.output = None
        self.task = None

    def retrieval(self, input: str):
        self.input = input
        self.task = "retrieval"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def generation(self, input: str):
        self.input = input
        self.task = "generation"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def router(self, input: str):
        self.input = input
        self.task = "router"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def event(self, input: str):
        self.input = input
        self.task = "event"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def system(self, input: str|object):
        self.input = str(input)
        self.task = "system"
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def end(self, output: str|object):
        self.output = str(output)
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()
    
    def _send_trace(self):
        self.client._trace(
            type="traces",
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            interaction_id=self.interaction_id,
            user=self.user,
            metadata=self.metadata,
            input=self.input,
            output=self.output,
            task=self.task,
            custom=str(self.custom),
            start_timestamp=self.start_timestamp * 1000,
            end_timestamp=self.end_timestamp * 1000
        )
        self.input = None
        self.output = None
        self.task = None
        self.start_timestamp = None
        self.end_timestamp = None