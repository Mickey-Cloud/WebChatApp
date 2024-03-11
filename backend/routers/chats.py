from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.schema import(
    ChatCollection,
    ChatUpdate,
    ChatResponse,    
    MessageCollection,
    UserCollection,
)


from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", response_model=ChatCollection)
def get_chats(
    sort: Literal["name", "id", "created_at"] = "name",
    session: Session = Depends(db.get_session)
    ):
    """Gets all the chats"""
    
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_chats(session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@chats_router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int,
    session: Session = Depends(db.get_session)
    ):
    """Get a chat for a given ID."""
    
    return ChatResponse(
        chat = db.get_chat_by_id(session, chat_id))


@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    session: Session = Depends(db.get_session)
    ):
    """Changes the name of the given chat"""
    
    return ChatResponse(
        chat = db.put_chat_name_update(session, chat_id, chat_update))

@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(
    chat_id: int,
    sort: Literal["id", "user_id", "created_at"] = "created_at",
    session: Session = Depends(db.get_session)
    ):
    """Gets all the messages pertaining to a specific Chat"""
    
    sort_key = lambda message: getattr(message, sort)
    messages = db.get_messages_by_chat_id(session, chat_id)
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_user_fosters(
    chat_id: int,
    sort: Literal["id", "created_at"] = "id",
    session: Session = Depends(db.get_session)
    ):
    """Gets all the Users associated with the specific chat"""
    
    sort_key = lambda user: getattr(user, sort)
    users = db.get_chat_users(session, chat_id)
    return UserCollection(
        meta ={"count": len(users)},
        users=sorted(users, key=sort_key)
    )