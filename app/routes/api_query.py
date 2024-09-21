from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from models.schemas import PromptCreate, ConversationFull, APIError
from db.db_query import create_prompt
from utils.openai import generate_response, OpenAIException
from db.db_conversations import add_message_to_conversation
from utils.errors import create_error_response
from beanie.exceptions import DocumentNotFound
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/query", tags=["query"])

@router.post("/{conversation_id}", responses={
  200: {
    "description": "Query successful",
    "model": Dict[str, str]
  },
  500: {
    "description": "Internal server error",
    "model": APIError
  },
  404: {
    "description": "Conversation not found",
    "model": APIError
  }
})
async def query_endpoint(conversation_id: str, query: PromptCreate) -> Dict[str, str]:
  """
  Query the LLM and return the response

  Args:
    id (str): The unique identifier for the query
    prompt (PromptCreate): The prompt object containing the query content
    
  Returns:
    str: The LLM's response
  
  Raises:
    - 404: If the conversation is not found
    - 500: If there was an unexpected server error
  """
  try:
    # create the prompt in the database
    created_prompt = await create_prompt(conversation_id, query)

    prompt_id = created_prompt["prompt_id"]
    message_tokens = created_prompt["tokens"]

    # add the query to the conversation and get the updated conversation messages
    conversation: ConversationFull = await add_message_to_conversation(conversation_id, prompt_id, message_tokens)

    # query the LLM
    prompt_response: PromptCreate = generate_response(conversation)

    # add the response to the conversation and get the updated conversation messages
    created_prompt_response = await create_prompt(conversation_id, prompt_response)
    prompt_id = created_prompt_response["prompt_id"]
    message_tokens = created_prompt_response["tokens"]

    # add the response to the conversation and get the updated conversation messages
    await add_message_to_conversation(conversation_id, prompt_id, message_tokens)

    return {
      "response": prompt_response.content
    }
  
  except DocumentNotFound as e:
    logging.error(f"Error querying LLM: {str(e)}")
    error = create_error_response(404, "Conversation not found", {"method": "POST", "url": "/query/" + conversation_id}, e)
    raise HTTPException(status_code=404, detail=error.dict())
  except OpenAIException as e:
    logging.error(f"Error querying LLM: {str(e)}")
    error = create_error_response(422, "Unable to create resource due to errors", {"method": "POST", "url": "/query/" + conversation_id}, e)
    raise HTTPException(status_code=422, detail=error.dict())
  except Exception as e: 
    logging.error(f"Error querying LLM: {str(e)}")
    error = create_error_response(500, "Internal Server Error", {"method": "POST", "url": "/query/" + conversation_id}, e)
    raise HTTPException(status_code=500, detail=error.dict())
