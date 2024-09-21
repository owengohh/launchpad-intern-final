from beanie import Document
from pydantic import Field
from typing import List
from uuid import uuid4
from enum import Enum
from typing import Dict

class QueryRoleType(str, Enum):
  system = "system"
  user = "user"
  assistant = "assistant"
  function = "function"

class Prompt(Document):
  id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", primary_key=True, description="Unique identifier for the prompt")
  role: QueryRoleType = Field(..., description="Role of the message sender")
  content: str = Field(..., description="Content of the message")
  conversation_id: str = Field(..., description="Unique identifier for the conversation")

  class Settings:
    collection = "prompts"

class Conversation(Document):
  id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", primary_key=True, description="Unique identifier for the conversation")
  name: str = Field(max_length=200, description="Name of the conversation")
  params: Dict[str, float] = Field(..., description="Parameter dictionary to override defaults prescribed by the AI Model")
  tokens: int = Field(ge=0, default=0, description="The number of tokens used in the conversation")
  messages: List[str] = Field(default_factory=list, description="Chat messages id included in the conversation")

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Example Conversation",
        "params": {"temperature": 0.7},
        "tokens": 1500,
        "messages": [
          {"role": "user", "content": "Hello!"},
          {"role": "assistant", "content": "Hi! How can I assist you today?"}
        ],
      }
    }

  class Settings:
    collection = "conversations"

    