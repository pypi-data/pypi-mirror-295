# Reference
<details><summary><code>client.<a href="src/NeuralTrust/client.py">trace</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a new trace
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from NeuralTrust.client import NeuralTrustApi

client = NeuralTrustApi(
    api_key="YOUR_API_KEY",
)
client.trace(
    conversation_id="conversation_id",
    interaction_id="interaction_id",
    type="type",
    task="retrieval",
    input="What is the weather in Tokyo?",
    start_timestamp="start_timestamp",
    end_timestamp="end_timestamp",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_id:** `str` — conversation id
    
</dd>
</dl>

<dl>
<dd>

**interaction_id:** `str` — interaction id
    
</dd>
</dl>

<dl>
<dd>

**type:** `str` — type of trace
    
</dd>
</dl>

<dl>
<dd>

**task:** `TraceTask` — task to perform
    
</dd>
</dl>

<dl>
<dd>

**input:** `str` — content to retrieve or generate
    
</dd>
</dl>

<dl>
<dd>

**start_timestamp:** `str` — start timestamp of the trace
    
</dd>
</dl>

<dl>
<dd>

**end_timestamp:** `str` — end timestamp of the trace
    
</dd>
</dl>

<dl>
<dd>

**session_id:** `typing.Optional[str]` — session id
    
</dd>
</dl>

<dl>
<dd>

**channel_id:** `typing.Optional[str]` — channel id
    
</dd>
</dl>

<dl>
<dd>

**output:** `typing.Optional[str]` — generated content
    
</dd>
</dl>

<dl>
<dd>

**custom:** `typing.Optional[str]` — custom data
    
</dd>
</dl>

<dl>
<dd>

**user:** `typing.Optional[User]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[Metadata]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

