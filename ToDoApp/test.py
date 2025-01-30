from ToDoApp.routers.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

# Ваши настройки
SECRET_KEY = "d1e749a332172f08a9eec6b9788a9695b74b27a8ec3f90a034c01c721578fc99"
ALGORITHM = "HS256"

# Тестовый токен
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5dXJpeSIsImlkIjoxLCJyb2xlIjoic3RyaW5nIiwiZXhwIjoxNzM2Nzg1NTM1fQ.OlXCT5uYSzetVrHj7aBaP4j57tXGr_4XD75LWznOVtA"

# Тестовая функция
async def test_get_current_user():
    try:
        user = await get_current_user(token=test_token)
        print(f"Decoded user: {user}")
    except Exception as e:
        print(f"Error: {e}")

# Запуск теста
import asyncio
asyncio.run(test_get_current_user())
