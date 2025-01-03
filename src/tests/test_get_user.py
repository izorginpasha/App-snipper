import httpx
import pytest
from unittest.mock import patch, AsyncMock
@pytest.mark.asyncio
async def test_get_user():
    # Данные для мокирования ответа внешнего API
    user_data = {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz"
    }
    # Мокируем метод `get` класса `AsyncClient` из `httpx`
    async def mock_get(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = user_data
        return mock_response
    with patch('httpx.AsyncClient.get', new=mock_get):
        async with httpx.AsyncClient() as ac:
            response = await ac.get("/users/1")
        assert response.status_code == 200
        response_json = await response.json()
        assert response_json == user_data