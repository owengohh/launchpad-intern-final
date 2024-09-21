from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum


class QueryRoleType(str, Enum):
  system = "system"
  user = "user"
  assistant = "assistant"
  function = "function"

class PromptBase(BaseModel):
  role: QueryRoleType
  content: str

class PromptCreate(PromptBase):
  pass

class PromptRead(PromptBase):
  id: str = Field(alias="_id")

  class Config:
    from_attributes = True

class ConversationBase(BaseModel):
  name: str = Field(..., max_length=200, description="Title of the conversation")
  params: Optional[Dict[str, float]] = Field(default_factory=dict, description="Parameter dictionary to override defaults prescribed by the AI Model")

class ConversationCreate(ConversationBase):
  pass
  
class ConversationUpdate(BaseModel):
  name: Optional[str] = Field(None, max_length=200, description="Title of the conversation")
  params: Optional[Dict[str, float]] = Field(default_factory=dict, description="Parameter dictionary to override defaults prescribed by the AI Model")

class ConversationRead(ConversationBase):
  id: str = Field(..., alias="_id")
  tokens: int = Field(default=0, ge=0, description="The number of tokens used in the conversation")

  class Config:
    from_attributes = True
    populate_by_name = True

# Conversation Full Schema
class ConversationFull(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field(..., max_length=200, description="Title of the conversation")
    params: Optional[Dict[str, float]] = Field(default_factory=dict, description="Parameter dictionary to override defaults prescribed by the AI Model")
    tokens: int = Field(default=0, ge=0, description="The number of tokens used in the conversation")
    messages: List[PromptRead] = Field(default_factory=list, description="Chat messages included in the conversation")

    class Config:
        from_attributes = True
        populate_by_name = True

# Error Schema
class APIError(BaseModel):
    code: int = Field(..., description="API error code")
    message: str = Field(..., description="Error message describing what went wrong")
    request: Optional[Dict] = Field(None, description="Details of the request that caused the error")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional information about the error")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "message": "Invalid parameters provided",
                "request": {"method": "POST", "url": "/conversations"},
                "details": {"field": "name"}
            }
        }