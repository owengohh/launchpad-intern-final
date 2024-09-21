from fastapi import APIRouter, status, HTTPException
from beanie.exceptions import DocumentNotFound
from db.db_conversations import create_conversation, get_all_conversations, get_conversation, update_conversation, delete_conversation
from typing import List, Dict
from models.schemas import ConversationCreate, ConversationFull, ConversationUpdate, ConversationRead, APIError
from utils.errors import create_error_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("", status_code=status.HTTP_201_CREATED, responses={
  201: {
    "description": "Conversation created successfully",
    "model": Dict[str, str]
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  },
  400: {
    "description": "Invalid parameter(s)",
    "model": APIError
  }
},
summary="Create a new conversation",
description="Create a new conversation with the given parameters")
async def create_conversation_endpoint(
    conversation: ConversationCreate
) -> Dict[str, str]:
  """
    Create a new conversation with the given details.

  Args:
    conversation (ConversationCreate): The details of the conversation to create

  Returns:
    Dict[str, str]: The ID of the newly created conversation

  Raises:

    Raises:
    - 400: If the conversation couldn't be created due to validation errors
    - 500: If there was an unexpected server error
  """
  try:
    db_id = await create_conversation(conversation)
    return {"id": db_id}
  except Exception as e:
    logging.error(f"Error creating conversation: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "POST", "url": "/conversations"}, e)
    raise HTTPException(status_code=500, detail=error.dict())

@router.get("", summary="Get all conversations", description="Retrieve all conversations from the database", responses={
  200: {
    "description": "Conversations retrieved successfully",
    "model": List[ConversationRead]
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  }
})
async def get_conversations_endpoint() -> List[ConversationRead]:
  """
  Get all conversations 

  Args:
    None

  Returns:
    List[ConversationRead]: A list of all conversations without their full conversation history

  Raises:
  - 500: If there was an unexpected server error
  """
  try:
    return await get_all_conversations()
  except Exception as e:
    logging.error(f"Error getting conversations: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "GET", "url": "/conversations"}, e)
    raise HTTPException(status_code=500, detail=error.dict())


@router.get("/{conversation_id}", summary="Get a conversation by ID", description="Retrieve a conversation by its unique identifier", responses={
  200: {
    "description": "Conversation retrieved successfully",
    "model": ConversationFull
  },
  404: {
    "description": "Conversation not found",
    "model": APIError
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  }
})
async def get_conversation_endpoint(conversation_id: str) -> ConversationFull:
  """
  Get a conversation by id

  Args:
    conversation_id (str): The unique identifier for the conversation

  Returns:
    ConversationFull: The conversation with the given id and its full conversation history

  Raises:
  - 404: If the conversation is not found
  - 500: If there was an unexpected server error
  """
  try:
    return await get_conversation(conversation_id)
  except DocumentNotFound as e:
    logging.error(f"Error getting conversation: {str(e)}")
    error = create_error_response(404, "Conversation not found", {"method": "GET", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=404, detail=error.dict())
  except Exception as e:
    logging.error(f"Error getting conversation: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "GET", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=500, detail=error.dict())

@router.put("/{conversation_id}", summary="Update a conversation by ID", description="Update a conversation by its unique identifier", responses={
  204: {
    "description": "Conversation updated successfully",
    "model": None
  },
  404: {
    "description": "Conversation not found",
    "model": APIError
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  },
  400: {
    "description": "Invalid parameter(s)",
    "model": APIError
  }
})
async def update_conversation_endpoint(
    conversation_id: str,
    conversation: ConversationUpdate
) -> None:
  """
  Update a conversation by id

  Args:
    conversation_id (str): The unique identifier for the conversation
    conversation (ConversationUpdate): The updated conversation details

  Returns:
    None

  Raises:
    - 400: If the conversation couldn't be updated due to validation errors
  - 404: If the conversation is not found
  - 500: If there was an unexpected server error
  """
  try:
    await update_conversation(conversation_id, conversation)  
  except DocumentNotFound as e:
    logging.error(f"Error updating conversation: {str(e)}")
    error = create_error_response(404, "Conversation not found", {"method": "PUT", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=404, detail=error.dict())
  except Exception as e:
    logging.error(f"Error updating conversation: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "PUT", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=500, detail=error.dict())

@router.delete("/{conversation_id}", summary="Delete a conversation by ID", description="Delete a conversation by its unique identifier", responses={
  204: {
    "description": "Conversation deleted successfully",
    "model": None
  },
  404: {
    "description": "Conversation not found",
    "model": APIError
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  }
})
async def delete_conversation_endpoint(conversation_id: str) -> None:
  """
  Delete a conversation by id

  Args:
    conversation_id (str): The unique identifier for the conversation

  Returns:
    None

  Raises:
  - 404: If the conversation is not found
  - 500: If there was an unexpected server error
  """
  try:
     await delete_conversation(conversation_id)
  except DocumentNotFound as e:
    logging.error(f"Error deleting conversation: {str(e)}")
    error = create_error_response(404, "Conversation not found", {"method": "DELETE", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=404, detail=error.dict())
  except Exception as e:
    logging.error(f"Error deleting conversation: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "DELETE", "url": "/conversations/" + conversation_id}, e)
    raise HTTPException(status_code=500, detail=error.dict())
