# NeuralTrust Python SDK

The NeuralTrust Python SDK provides a convenient way to interact with the NeuralTrust API. It allows you to manage conversations, send messages, and trace interactions asynchronously.

## Installation

To install the SDK, use pip:

```bash
pip install neuraltrust
```

## Usage

### Initialization

First, initialize the `NeuralTrust` client with your API key:

```python
from neuraltrust.client import NeuralTrust

client = NeuralTrust(api_key="your_api_key")
```

You can also set the `base_url`, `timeout`, and `max_workers` if needed:

```python
client = NeuralTrust(
    api_key="your_api_key",
    timeout=30.0,
    max_workers=10
)
```

### Timeout and Max Workers

#### Timeout
The `timeout` parameter specifies the maximum amount of time (in seconds) that the SDK will wait for a response from the NeuralTrust API before timing out. This is useful to ensure that your application does not hang indefinitely while waiting for a response. You can set this value when initializing the `NeuralTrust` client:

```python
client = NeuralTrust(
    api_key="your_api_key",
    timeout=30.0,  # Timeout set to 30 seconds
    max_workers=10
)
```

#### Max Workers
The `max_workers` parameter determines the maximum number of threads that will be used by the `ThreadPoolExecutor` for handling asynchronous tasks. This is useful for managing the concurrency of API requests, allowing multiple requests to be processed in parallel. You can set this value when initializing the `NeuralTrust` client:

```python
client = NeuralTrust(
    api_key="your_api_key",
    timeout=30.0,
    max_workers=10  # Maximum of 10 worker threads
)
```

These parameters help in optimizing the performance and responsiveness of your application when interacting with the NeuralTrust API.

### Creating and Sending Traces

To create a new trace:

```python
trace = client.trace(
    conversation_id="conv_1234",
    session_id="sess_123",
    user=User(user_id="user_123"),
    metadata=Metadata(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        timezone="America/New_York"
    ),
    custom={"custom_field": "custom_value"}
)
```
### Trace Class

The `Trace` class allows you to create and manage traces. Here are the available options:

- `conversation_id` (str): The unique identifier of the conversation.
- `session_id` (Optional[str]): The unique identifier of the session.
- `custom` (Optional[dict]): Custom data.
- `user` (Optional[User]): The user information.
- `metadata` (Optional[Metadata]): The metadata information.

### Metadata Class

The `Metadata` class allows you to provide additional information about the user's environment. Here are the available options:

- `user_agent` (Optional[str]): The user agent string of the browser. If provided, `os` and `browser` can be inferred and are not necessary.
- `timezone` (Optional[str]): The timezone of the user. If provided, `location` can be inferred and is not necessary.
- `browser` (Optional[str]): The browser used by the user.
- `device` (Optional[str]): The device used by the user.
- `os` (Optional[str]): The operating system of the user's device.
- `locale` (Optional[str]): The locale of the user.
- `location` (Optional[str]): The location of the user.

### User Class

The `User` class allows you to provide information about the user. Here are the available options:

- `user_id` (Optional[str]): The unique identifier of the user.
- `user_email` (Optional[str]): The email address of the user.
- `user_phone` (Optional[str]): The phone number of the user.


### Trace Types

The `Trace` class supports different types of traces, each serving a specific purpose:

- **Retrieval**: Used when retrieving information from the embedding vector database based on user input.
- **Generation**: Used when generating a response or content based on user input.
- **Router**: Used when routing a user's query to the appropriate handler or service.
- **System**: Used for system prompts that utilize the LLM to generate content.

Here is how you can use each trace type:

#### Retrieval Trace
```python
trace.retrieval("What is my name?")
trace.end([
    {"name": "John Doe", "similarity": 0.95},
    {"name": "Jane Smith", "similarity": 0.82},
    {"name": "John Smith", "similarity": 0.78}
])
```

#### Generation Trace
```python
trace.generation("Hello, how are you?")
trace.end("I'm good, thank you!")
```

#### Router Trace
```python
trace.router("What is my name?")
trace.end({
    "route": "name_agent",
    "confidence": 0.95,
    "metadata": {
        "intent": "name_inquiry",
        "entities": ["name"]
    }
})
```

#### System Trace
```python
trace.system("System prompt or command")
```

### Full Example

Here is a full example of how to interact with the SDK:

```python
from neuraltrust import NeuralTrust
from neuraltrust.api_client.types import User, Metadata

# Initialize the NeuralTrust client with your API key
API_KEY = "your_api_key"
client = NeuralTrust(api_key=API_KEY)

# Create a user object with more detailed information
user = User(
    user_id="user_123"
)

# Create metadata with additional details
metadata = Metadata(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    timezone="America/New_York"
)

# Start a new trace for a conversation
trace = client.trace(
    conversation_id="conv_1234",
    session_id="sess_123",
    user=user,
    metadata=metadata,
    custom={"custom_field": "custom_value"}
)

# Simulate a user sending a message and the bot generating a response
trace.generation("Hello, how are you?")
trace.end("I'm good, thank you!")

# Simulate a user asking for their name and the bot retrieving it
trace.retrieval("What is my name?")
trace.end([
    {"name": "John Doe", "similarity": 0.95},
    {"name": "Jane Smith", "similarity": 0.82},
    {"name": "John Smith", "similarity": 0.78}
])

# Simulate a routing decision based on user input
trace.router("What is my name?")
trace.end({
    "route": "name_agent",
    "confidence": 0.95,
    "metadata": {
        "intent": "name_inquiry",
        "entities": ["name"]
    }
})
```

## License

MIT License

Copyright (c) 2024 NeuralTrust

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.