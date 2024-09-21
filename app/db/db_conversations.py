from models.models import Conversation, Prompt, QueryRoleType
from models.schemas import ConversationCreate, ConversationUpdate, ConversationFull, PromptRead, ConversationRead
from beanie.exceptions import DocumentNotFound
from beanie import Link
import logging
from typing import List

logger = logging.getLogger(__name__)

async def create_conversation(conversation: ConversationCreate) ->  str:
  """
  Create a new conversation in the database

  Args:
    conversation (ConversationCreate): The details of the conversation to create

  Returns:
    str: The id of the newly created conversation

  Raises:
    - Exception: If there was an unexpected server error
  """
  try:
    db_conversation = Conversation(
            name=conversation.name,
            params=conversation.params,
            tokens=0  # Initialize with 0 tokens
    )

    await db_conversation.insert()

    # return the conversation id
    return db_conversation.id
  except Exception as e:
    logger.error(f"Database error creating conversation: {str(e)}")
    raise

async def get_conversation(conversation_id: str) -> ConversationFull:
  """
  Get a conversation by id and return its full conversation history

  Args:
    conversation_id (str): The unique identifier for the conversation

  Returns:
    ConversationFull: The conversation with the given id and its full conversation history

  Raises:
    - DocumentNotFound: If the conversation is not found
  """
  try:
    db_conversation = await Conversation.get(conversation_id, fetch_links=True)
    if db_conversation is None:
      raise DocumentNotFound(f"Conversation with ID {conversation_id} not found")
    
    # return the conversation
    return await get_conversation_full(db_conversation.id)
  except DocumentNotFound as e:
    logger.error(f"Document not found getting conversation {conversation_id}: {str(e)}")
    raise
  
async def get_all_conversations() -> List[ConversationRead]:
  """
  Get all conversations and return the conversations details without the conversation history

  Returns:
    List[ConversationRead]: The conversations with the given id and its full conversation history

  Raises:
    - Exception: If there was an unexpected server error
  """
  try:
    db_conversations = await Conversation.find_all().to_list()
    conversation_reads = [ConversationRead(
      id=conversation.id,
      name=conversation.name,
      params=conversation
      .params,
      tokens=conversation.tokens
    ) for conversation in db_conversations]
    
    # return the conversations
    return conversation_reads

  except Exception as e:
    logger.error(f"Database error getting all conversations: {str(e)}")
    raise

async def update_conversation(conversation_id: str, conversation: ConversationUpdate) -> str:
  """
  Update a conversation by id and return a success message

  Args:
    conversation_id (str): The unique identifier for the conversation
    conversation (ConversationUpdate): The details of the conversation to update

  Returns:
    str: A success message
  """
  try:
    db_conversation = await Conversation.get(conversation_id)
    if db_conversation is None:
      raise DocumentNotFound(f"Conversation with ID {conversation_id} not found")

    # Update conversation
    update_data = conversation.dict(exclude_unset=True)
    for key, value in update_data.items():
      setattr(db_conversation, key, value)
    
    # save the updated conversation
    await db_conversation.save()

    # return the updated conversation
    return "conversation updated successfully"
  
  except DocumentNotFound as e:
    logger.error(f"Document not found: {str(e)}")
    raise
  except Exception as e:
    logger.error(f"Database error: {str(e)}")
    raise

async def delete_conversation(conversation_id: str) -> str:
  """
  Delete a conversation by id and return a success message

  Args:
    conversation_id (str): The unique identifier for the conversation

  Returns:
    str: A success message
  """
  try:
    db_conversation = await Conversation.get(conversation_id)
    if db_conversation is None:
      raise DocumentNotFound(f"Conversation with ID {conversation_id} not found")
    
    # delete all messages in the conversation
    await Prompt.find({"conversation_id": conversation_id}).delete()

    # delete the conversation
    await db_conversation.delete()
  except DocumentNotFound as e:
    logger.error(f"Document not found deleting conversation {conversation_id}: {str(e)}")
    raise
  except Exception as e:
    logger.error(f"Database error deleting conversation {conversation_id}: {str(e)}")
    raise

  return "conversation deleted successfully"

async def add_message_to_conversation(conversation_id: str, prompt_id: str, message_tokens: int) -> ConversationFull:
  """
  Add a message to a conversation and return the updated conversation

  Args:
    conversation_id (str): The unique identifier for the conversation
    prompt_id (str): The unique identifier for the prompt
    message_tokens (int): The number of tokens in the message

  Returns:
    ConversationFull: The updated conversation
  """
  try:
    db_conversation = await Conversation.get(conversation_id, fetch_links=True)
    if db_conversation is None:
            raise DocumentNotFound(f"Conversation with ID {conversation_id} not found")
    
    # add the new message to the conversation
    db_conversation.messages.append(prompt_id)

    # update the conversation's token count
    db_conversation.tokens += message_tokens

    # save the updated conversation
    await db_conversation.save()

      # fetch the updated conversation
    return await get_conversation_full(conversation_id)

  except DocumentNotFound as e:
      logger.error(f"Document not found adding message to conversation {conversation_id}: {str(e)}")
      raise
  except Exception as e:
      logger.error(f"Database error adding message to conversation {conversation_id}: {str(e)}")
      raise 

async def get_conversation_full(conversation_id: str) -> ConversationFull:
  """
  Get a conversation by id and return its full conversation history

  Args:
    conversation_id (str): The unique identifier for the conversation

  Returns:
    ConversationFull: The conversation with the given id and its full conversation history
  """
  db_conversation = await Conversation.get(conversation_id)
  if db_conversation is None:
    raise DocumentNotFound(f"Conversation with ID {conversation_id} not found")
  prompts = await Prompt.find(Prompt.conversation_id == db_conversation.id).to_list()
  prompt_reads = [PromptRead.model_validate(prompt.dict(by_alias=True)) for prompt in prompts]
  
  message_id_order = {str(msg_id): index for index, msg_id in enumerate(db_conversation.messages)}
  prompt_reads.sort(key=lambda x: message_id_order.get(x.id, float('inf')))

  return ConversationFull(
    id=db_conversation.id,
    name=db_conversation.name,
    params=db_conversation.params,
    tokens=db_conversation.tokens,
    messages=prompt_reads
  )
