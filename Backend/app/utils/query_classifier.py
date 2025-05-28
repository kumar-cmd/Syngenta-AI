from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from typing import Optional, List
import requests
import json
from app.config import Config

# 👇 Step 1: Custom LangChain-compatible LLM using your Lambda Claude API
class CustomBedrockLLM(LLM):
    url: str
    api_key: str
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 100

    @property
    def _llm_type(self) -> str:
        return "custom-bedrock-claude"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            "api_key": self.api_key,
            "prompt": prompt,
            "model_id": self.model_id,
            "model_params": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")

        return response.json()["response"]["content"][0]["text"]


# 👇 Step 2: Setup your LLM
llm = CustomBedrockLLM(
    url="https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/",
    api_key=Config.BEDROCK_API_KEY,  # 🔐 Replace this
    model_id="claude-3.5-sonnet"
)




# Create a RunnableSequence chaining prompt and LLM


# Call invoke() instead of run()



# 👇 Step 3: Create the prompt template
prompt_template = PromptTemplate.from_template("""
You are a smart classifier. Categorize the following user query into one of these:

- "document" (unstructured text: summarize, extract, QA from documents)
- "sql" (structured data: tables, filters, group by, aggregates)
- "hybrid" (combines document and structured data)

Respond ONLY with: document, sql, or hybrid.

User query: {query}
""")

# 👇 Step 4: Build the classifier chain
classifier_chain = prompt_template | llm


def queryClassifier(query):
    result = classifier_chain.invoke(query).strip().lower()
    return result

