from neuraltrust import NeuralTrust
from neuraltrust.api_client.types import User, Metadata

NEURALTRUST_API_KEY = "f6baad57-722a-4265-8ea0-bf5e8836aed3:4559e47b751ec762a5cfd635d8e98e205120104b3b0d0b4be504c992812c4f40"
NEURALTRUST_BASE_URL = "https://api.neuraltrust.ai"

client = NeuralTrust(api_key=NEURALTRUST_API_KEY, base_url=NEURALTRUST_BASE_URL)

user = User(
    user_id="user_123",
    user_email="user@example.com",
    user_phone="+1234567890"
)

# Create metadata with additional details
metadata = Metadata(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    timezone="America/New_York"
)

# Start a new trace for a conversation
trace = client.trace(
    conversation_id="conv_123454656",
    channel_id="web",
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

trace.system({"system": "You are a helpful assistant."})