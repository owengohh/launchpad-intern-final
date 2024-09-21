import os
from openai import OpenAI
from models.schemas import ConversationFull, PromptCreate

class OpenAIException(Exception):
    pass

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_response(conversation: ConversationFull) -> str:
  """
  Generate a response from the LLM
  """

  messages_list = [{"role": message.role, "content": message.content} for message in conversation.messages]

  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages_list,
      **conversation.params
    )
    return PromptCreate(content=response.choices[0].message.content.strip(), role="assistant")
  except Exception as e:
    print(f'Error generating response: {e}')
    raise OpenAIException(f"Error generating response: {e}")
