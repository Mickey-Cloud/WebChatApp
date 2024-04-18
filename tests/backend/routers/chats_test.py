from datetime import date

from fastapi.testclient import TestClient

from backend.main import app  

# --------------------- Chat Tests ------------------------ #


def test_get_all_chats(client, default_database ):
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])


def test_get_chat(client, default_database):
    
    chatId = 1
    response = client.get(f"/chats/{chatId}")
    assert response.status_code == 200
    
    user = response.json()
    assert user['chat']['id'] == chatId

def test_get_chat_dne(client, default_database):
    
    chatId = 0
    response = client.get(f"/chats/{chatId}")
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chatId
        }
    }

def test_put_chat_dne(client, default_database):
    
    chatId = 0
    create_params= {
        "name": "Updated Name",
    }
    response = client.put(f"/chats/{chatId}", json=create_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chatId
        }
    }

def test_put_chat(client, default_database):
    
    chatId = 1
    create_params= {
        "name": "Updated Name",
    }
    response = client.put(f"/chats/{chatId}", json=create_params)
    assert response.status_code == 200
    
    chat = response.json()['chat']
    for key, value in create_params.items():
        assert chat[key] == value
    
    response = client.get(f"/chats/{chatId}")
    assert response.status_code == 200
    
    chat = response.json()['chat']
    for key, value in create_params.items():
        assert chat[key] == value

def test_get_chat_messages(client, default_database):
    
    chatId = 1
    response = client.get(f"/chats/{chatId}/messages")
    assert response.status_code == 200
    
    meta = response.json()["meta"]
    messages = response.json()["messages"]
    assert meta["count"] == len(messages)
    assert messages == sorted(messages, key=lambda message: message["created_at"])
    
    
def test_get_chat_messages_DNE(client, default_database):
    
    chatId = 0
    response = client.get(f"/chats/{chatId}/messages")
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chatId
        }
    }

def test_get_chat_users(client, default_database):
    
    chatId = 1
    response = response = client.get(f"/chats/{chatId}/users")
    assert response.status_code == 200
    
    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_get_chat_users_dne(client, default_database):
    
    chatId = 0
    response = client.get(f"/chats/{chatId}/users")
    assert response.status_code == 404
    assert response.json() == {
        "detail":{
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chatId
        }
    }

def test_delete_user_chat_link(default_database, logged_in_client ):
    message = {
        'text': "new message"
    }
    response = logged_in_client.delete("/chats/1/users/2")
    assert response.status_code == 200
