"""
測試設定：用 mongomock_motor 模擬 MongoDB，
不需要真實資料庫即可測試 motor 非同步存取的邏輯。
"""
import os

os.environ.setdefault("MONGODB_URL", "mongodb://localhost:27017")
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_pytest")

import pytest
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient

import main
import routers.user as user_router


@pytest.fixture
def client():
    # 每個測試換上乾淨的 mock db（routes 透過 routers.user.db 取用）
    user_router.db = AsyncMongoMockClient()["coda_test"]
    with TestClient(main.app) as c:
        yield c


@pytest.fixture
def auth_headers(client):
    client.post("/api/user/register", json={
        "name": "Tester", "email": "tester@example.com", "password": "pw123456",
    })
    res = client.post("/api/user/login", json={
        "email": "tester@example.com", "password": "pw123456",
    })
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
