import os
os.environ['ENVIRONMENT'] = 'testing'
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from models.models import Conversation, Prompt
from models.schemas import ConversationFull, PromptCreate
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
import logging

from main import app  # Adjust based on your project structure

@pytest.mark.asyncio
async def test_get_conversations():
    # Mock the get_all_conversations function
    with patch('routes.api_conversations.get_all_conversations', new_callable=AsyncMock) as mock_get_all:
        # Define what the mock should return
        mock_get_all.return_value = [
            {
                "_id": "1",
                "name": "Test Conversation",
                "params": {"test": 0.1},
                "tokens": 0
            }
        ]

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/conversations")
            print(response.json())

        assert response.status_code == 200
        assert response.json() == mock_get_all.return_value
        mock_get_all.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_conversation():
    # Mock the get_conversation function
    with patch('routes.api_conversations.get_conversation', new_callable=AsyncMock) as mock_get_by_id:
        # Define what the mock should return
        mock_get_by_id.return_value = {
            "_id": "1",
            "name": "Test Conversation",
            "params": {"test": 0.1},
            "tokens": 0,
            "messages": []
        }

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/conversations/1")
            print(response.json())

        assert response.status_code == 200
        assert response.json() == mock_get_by_id.return_value
        mock_get_by_id.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_conversation():
    # Mock the create_conversation function
    with patch('routes.api_conversations.create_conversation', new_callable=AsyncMock) as mock_create:
        # Define what the mock should return
        mock_create.return_value = '1'

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.post("/conversations", json={
                "name": "Test Conversation",
                "params": {"test": 0.1}
            })
            print(response.json())

        assert response.status_code == 201
        assert response.json() == {'id': '1'}
        mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_conversation():
    # Mock the update_conversation function
    with patch('routes.api_conversations.update_conversation', new_callable=AsyncMock) as mock_update:
        # Define what the mock should return
        mock_update.return_value = {
            "_id": "1",
            "name": "Updated Conversation",
            "params": {"test": 0.2},
        }

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.put("/conversations/1", json={
                "name": "Updated Conversation",
                "params": {"test": 0.2}
            })
            print(response.json())

        assert response.status_code == 200
        assert response.json() == None
        mock_update.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_conversation():
    # Mock the delete_conversation function
    with patch('routes.api_conversations.delete_conversation', new_callable=AsyncMock) as mock_delete:
        # Define what the mock should return
        mock_delete.return_value = None

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.delete("/conversations/1")
            print(response.json())

        assert response.status_code == 200
        assert response.json() == None
        mock_delete.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_prompt():
    conversation_id = "test_id"
    query = PromptCreate(content="Test query", role="user")

    # Mock all the function calls
    with patch('routes.api_query.create_prompt', new_callable=AsyncMock) as mock_create_prompt, \
         patch('routes.api_query.add_message_to_conversation', new_callable=AsyncMock) as mock_add_message, \
         patch('routes.api_query.generate_response') as mock_generate_response:

        # Set up return values for the mocks
        mock_create_prompt.side_effect = [
            {"prompt_id": "prompt1", "tokens": 10},  # For the query
            {"prompt_id": "prompt2", "tokens": 15}   # For the response
        ]
        mock_add_message.return_value = ConversationFull(id=conversation_id, name="Test Conversation", params={}, tokens=0, messages=[])
        mock_generate_response.return_value = PromptCreate(content="Test response", role="assistant")

        # Make the request
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.post(f"/query/{conversation_id}", json=query.dict())

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"response": "Test response"}

        # Verify that our mocked functions were called with the expected arguments
        mock_create_prompt.assert_any_call(conversation_id, query)
        mock_add_message.assert_any_call(conversation_id, "prompt1", 10)
        mock_generate_response.assert_called_once()
        mock_create_prompt.assert_any_call(conversation_id, PromptCreate(content="Test response", role="assistant"))
        mock_add_message.assert_any_call(conversation_id, "prompt2", 15)

    
            