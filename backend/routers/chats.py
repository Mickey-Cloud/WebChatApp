from datetime import date
from typing import Literal

from fastapi import APIRouter

from backend.entities import (
    Chat,
    ChatCollection,
    ChatUpdate,
    MessageCollection,
    UserCollection,
)

from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", response_model=ChatCollection)
def get_chats(
    sort: Literal["name", "id", "created_at"] = "name"
    ):
    
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_chats()
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@chats_router.get("/{chat_id}", response_model=Chat)
def get_chat(chat_id: str):
    """Get a chat for a given ID."""
    
    return db.get_chat_by_id(chat_id)


@chats_router.put("/{chat_id}", response_model=Chat)
def update_chat(chat_id: str, chat_update: ChatUpdate):
    """Changes the name of the given chat"""
    
    return db.put_chat_name_update(chat_id, chat_update)


@chats_router.delete(
    "/{chat_id}",
    status_code=204,
    response_model=None
    )
def delete_user(chat_id: str):
    """
    Deletes a chat by the given ID

    Args:
        chat_id (str): The ID of the chat to be deleted.
    """
    db.delete_chat(chat_id)

@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(
    chat_id: str,
    sort: Literal["id", "user_id", "created_at"] = "created_at"
    ):
    
    sort_key = lambda message: getattr(message, sort)
    messages = db.get_messages_by_chat_id(chat_id)
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_user_fosters(
    chat_id: str,
    sort: Literal["id", "created_at"] = "id",
    ):
    
    sort_key = lambda user: getattr(user, sort)
    users = db.get_chat_users(chat_id)
    return UserCollection(
        meta ={"count": len(users)},
        users=sorted(users, key=sort_key)
    )