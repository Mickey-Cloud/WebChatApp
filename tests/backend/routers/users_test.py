from datetime import date, datetime

import pytest

from fastapi.testclient import TestClient

from backend.main import app  
from backend.schema import UserInDB  

@pytest.fixture
def default_users():
    return{
        UserInDB(
            id=1,
            username="miguel",
            email="migi@test.com",
            hashed_password="password123",
            created_at= datetime.now()
        ),
        
    }

# --------------- User Tests -------------------- #
def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_create_user():
    create_params = {
        "username": "JimmyFallon",
        "email": "email@test.com",
        "password": "password",
    }
    client = TestClient(app)
    response = client.post("/users", json=create_params)
    
    assert response.status_code == 200
    user = response.json()['user']
    for key, value in create_params.items():
        assert user[key] == value
        
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    user = response.json()['user']
    for key, value in create_params.items():
        assert user[key] == value

def test_create_duplicate_user():
    client = TestClient(app)
    userId = 1
    response = client.get(f"/users/{userId}")
    assert response.status_code == 200
    user = response.json()['user']
    
    create_params = {
        "id": f"{user['id']}",
    }
    client = TestClient(app)
    response = client.post("/users", json = create_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail":{
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": f"{user['id']}"
        }
    }

def test_get_user():
    client = TestClient(app)
    userId = 1
    response = client.get(f"/users/{userId}")
    assert response.status_code == 200
    
    user = response.json()['user']
    assert user['id'] == userId

def test_get_user_dne():
    client = TestClient(app)
    userId = 0
    response = client.get(f"/users/{userId}")
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": userId
        }
    }

def test_get_user_chats():
    client = TestClient(app)
    userId = 1
    response = client.get(f"/users/{userId}/chats")
    
    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_user_dne_get_user_chats():
    client = TestClient(app)
    userId = 0
    response = client.get(f"/users/{userId}/chats")
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": userId
        }
    }


