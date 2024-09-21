import tiktoken
from models.models import Conversation, Prompt
from models.schemas import PromptCreate

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count the number of tokens in a given text."""
    try:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
    except KeyError:
        print(f"Warning: model {model} not found. Using cl100k_base encoding.")
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

async def count_message_tokens(message: PromptCreate, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens for a single message."""
    tokens = count_tokens(message.content, model)
    if message.role:
        tokens += count_tokens(message.role, model)
    return tokens