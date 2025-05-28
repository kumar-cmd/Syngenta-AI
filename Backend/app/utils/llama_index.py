from llama_index.core.embeddings import BaseEmbedding
# from typing import List
import requests
import json
import asyncio
from pydantic import Field # Import Field from pydantic


from llama_index.core.llms.llm import LLM  # Import the specific LLM type
from llama_index.core.llms import CompletionResponse, LLMMetadata, ChatResponse
from llama_index.core.base.llms.types import ChatMessage, MessageRole, CompletionResponseGen, ChatResponseGen
from typing import Any, Dict, Sequence, List, Optional, Iterator
from llama_index.core.bridge.pydantic import PrivateAttr

from llama_index.core import StorageContext, load_index_from_storage
from app.config import Config

BEDROCK_API_KEY = Config.BEDROCK_API_KEY


class CustomAmazonEmbedding(BaseEmbedding):
    # Define api_key and url as Pydantic fields
    api_key: str = Field(..., description="API key for the embedding service")
    url: str = Field(..., description="Endpoint URL for the embedding service")

    def __init__(self, api_key: str, url: str):
        # Pydantic handles the assignment of api_key and url
        # Initialize parent class with required parameters
        super().__init__(
            api_key=api_key, # Pass api_key to the parent constructor if needed by BaseEmbedding
            url=url, # Pass url to the parent constructor if needed by BaseEmbedding
            model_name="amazon-embedding-v2",
            embed_batch_size=10  # Default batch size for embeddings
        )

    def _get_text_embedding(self, text: str) -> List[float]:
        payload = {
            "api_key": self.api_key,
            "prompt": text,
            "model_id": "amazon-embedding-v2"
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        return result["response"]["embedding"]

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Implement the required method for batch processing
        return [self._get_text_embedding(text) for text in texts]

    def _get_query_embedding(self, query: str) -> List[float]:
        # Implement the required method for query embeddings
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        # Implement the async version
        # For this example, we'll just call the sync method.
        # In a real async implementation, you would use an async http client.
        return self._get_query_embedding(query)





# Change the base class from BaseLLM to LLM
class CustomBedrockLikeLLM(LLM):
    """Custom LLM for a Bedrock-like API."""

    _api_key: str = PrivateAttr()
    _url: str = PrivateAttr()
    _model_id: str = PrivateAttr()

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            model_name=self._model_id,
        )

    def __init__(self, api_key: str, url: str, model_id: str = "claude-3.5-sonnet", **kwargs: Any):
        """Initialize the custom LLM."""
        super().__init__(**kwargs)
        self._api_key = api_key
        self._url = url
        self._model_id = model_id

    def _get_payload(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Helper to create the API payload."""
        return {
            "api_key": self._api_key,
            "prompt": prompt,
            "model_id": self._model_id,
            "model_params": {
                "max_tokens": kwargs.get("max_tokens", self.metadata.num_output if self.metadata.num_output is not None else 500),
                "temperature": kwargs.get("temperature", 0.7),
                **kwargs.get("model_params", {})
            }
        }

    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to send the POST request."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self._url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e

    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Get a completion from the custom LLM."""
        payload = self._get_payload(prompt, **kwargs)
        result = self._send_request(payload)
        generated_text = result.get("response", {}).get("content", [{}])[0].get("text", "")
        return CompletionResponse(text=generated_text)

    async def acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Asynchronously get a completion."""
        return await asyncio.to_thread(self.complete, prompt, **kwargs)

    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        """Chat with the custom LLM."""
        prompt = "\n".join([f"{m.role}: {m.content}" for m in messages])
        if messages[-1].role != MessageRole.ASSISTANT:
             prompt += "\n" + str(MessageRole.ASSISTANT) + ":"

        completion_response = self.complete(prompt, **kwargs)
        assistant_message = ChatMessage(role=MessageRole.ASSISTANT, content=completion_response.text)
        return ChatResponse(message=assistant_message)

    async def achat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        """Asynchronously chat."""
        return await asyncio.to_thread(self.chat, messages, **kwargs)

    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """Stream completion from the custom LLM."""
        completion_response = self.complete(prompt, **kwargs)
        yield completion_response

    async def astream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """Asynchronously stream completion."""
        completion_response = await self.acomplete(prompt, **kwargs)
        yield completion_response

    def stream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        """Stream chat from the custom LLM."""
        chat_response = self.chat(messages, **kwargs)
        yield chat_response

    async def astream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        """Asynchronously stream chat."""
        chat_response = await self.achat(messages, **kwargs)
        yield chat_response

    def _as_query_component(self) -> Any:
        """Return itself as a query component."""
        return self



from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
# Import the corrected CustomBedrockLikeLLM which inherits from LLM
# from __main__ import CustomBedrockLikeLLM # Assuming the class is defined in the main notebook context

# Assuming CustomAmazonEmbedding is already defined in previous cells

# Instantiate your custom embedding model
embedding_model = CustomAmazonEmbedding(
    api_key=BEDROCK_API_KEY,
    url="https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/"
)

# Configure settings using the new Settings class for embedding
Settings.embed_model = embedding_model

# Instantiate your custom LLM using the updated class
custom_llm = CustomBedrockLikeLLM(
    api_key=BEDROCK_API_KEY,
    url="https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/",
    model_id="claude-3-haiku"
)

# --- Diagnostic Print ---
# This check should now pass
from llama_index.core.llms.llm import LLM
print(f"Is custom_llm an instance of LLM? {isinstance(custom_llm, LLM)}")

# Configure Settings to use your custom LLM
Settings.llm = custom_llm





storage_context = StorageContext.from_defaults(persist_dir="/home/syngentai/mysite/app/vector_store")

index_loaded2 = load_index_from_storage(storage_context)




def query_documents(query):
    query_engine = index_loaded2.as_query_engine()
    response = query_engine.query(query)

    return {
        "answer": str(response),
        "sources": [
            {
                "text": node.node.get_text(),
                "metadata": node.node.metadata
            } for node in response.source_nodes
        ]
    }




