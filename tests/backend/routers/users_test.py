from datetime import date, datetime

import pytest

from fastapi.testclient import TestClient

from backend.main import app  
from backend.schema import UserInDB  

# --------------- User Tests -------------------- #
def test_get_all_users(client, session, default_users):
    session.add_all(default_users)
    session.commit()
    
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_create_user(client, session, default_users):
    session.add_all(default_users)
    session.commit()
    create_params = {
        "username": "jimmyfallon",
        "email": "jimmy@test.com",
        "password": "jimmy123",
    }
    
    response = client.post("/auth/registration", json=create_params)
    
    assert response.status_code == 200
    user = response.json()['user']
    partial_create_params={
        "username": "jimmyfallon",
        "email": "jimmy@test.com",
    }
    for key, value in partial_create_params.items():
        assert user[key] == value
        
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    user = response.json()['user']
    
    
    for key, value in partial_create_params.items():
        assert user[key] == value

def test_create_duplicate_user(client, session, default_users):
    session.add_all(default_users)
    session.commit()
    userId = 1
    response = client.get(f"/users/{userId}")
    assert response.status_code == 200
    user = response.json()['user']
    
    create_params = {
        "username": user['username'],
        "email": user['email'],
        "password": "richard123"
    }
    
    response = client.post("/auth/registration", json = create_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail":{
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "username",
            "entity_value": f"{user['username']}"
        }
    }
    
    create_params = {
        "username": "NotInDB",
        "email": user['email'],
        "password": "richard123"
    }
    
    response = client.post("/auth/registration", json = create_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail":{
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "email",
            "entity_value": f"{user['email']}"
        }
    }

def test_get_user(client, session, default_users):
    session.add_all(default_users)
    session.commit()
    userId = 1
    response = client.get(f"/users/{userId}")
    assert response.status_code == 200
    
    user = response.json()['user']
    assert user['id'] == userId

def test_get_user_dne(client, session, default_users):
    session.add_all(default_users)
    session.commit()
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

def test_get_user_chats(client, session, default_users):
    session.add_all(default_users)
    session.commit()
    userId = 1
    response = client.get(f"/users/{userId}/chats")
    
    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_user_dne_get_user_chats(client, session, default_users):
    session.add_all(default_users)
    session.commit()
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


