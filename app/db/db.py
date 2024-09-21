from motor.motor_asyncio import AsyncIOMotorClient
import os
from beanie import init_beanie
from models.models import Conversation, Prompt 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store client and database globally but don't initialize them immediately
client = None
database = None

def get_database():
    """
    Lazily initialize the MongoDB client and return the database.
    This prevents initialization at the module level.
    """
    global client, database
    if client is None:
        MONGO_URI = os.environ.get("MONGODB_URI")
        MONGODB_NAME = os.environ.get("MONGODB_NAME")
        client = AsyncIOMotorClient(MONGO_URI)
        database = client[MONGODB_NAME]
    return database

async def init_db() -> None:
    try:
        # Initialize the database only when this function is called
        db = get_database()
        await init_beanie(database=db, document_models=[Conversation, Prompt])
        logger.info("Beanie initialization completed")
    except Exception as e:
        logger.error(f"Failed to initialize Beanie: {str(e)}")
        raise

def close_connection() -> None:
    if client:
        client.close()
        logger.info("Connection closed")
