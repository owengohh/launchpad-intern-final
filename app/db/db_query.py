from models.schemas import PromptCreate
from models.models import Prompt, QueryRoleType
from utils.token_counter import count_message_tokens
import logging
from typing import Dict, Union
from utils.anonymise import anonymise
logger = logging.getLogger(__name__)

async def create_prompt(conversation_id: str, prompt: PromptCreate) -> Dict[str, Union[str, int]]:
  """
  Create a prompt in the database

  Args:
    conversation_id (str): The unique identifier for the conversation
    prompt (PromptCreate): The prompt object containing the query content

  Returns:
    Dict[str, Union[str, int]]: The prompt id and the number of tokens in the prompt
  """
  try:
    # anonymise content
    prompt.content = anonymise(prompt.content)

    # create a new prompt
    db_prompt = Prompt(
      role=QueryRoleType(prompt.role),
      content=prompt.content,
      conversation_id=conversation_id
    )
    await db_prompt.insert()

    # count tokens for the new message
    message_tokens = await count_message_tokens(prompt)

    return {
      "prompt_id": db_prompt.id,
      "tokens": message_tokens
    }
  
  except Exception as e:
    logger.error(f"Database error creating prompt: {str(e)}")
    raise 

