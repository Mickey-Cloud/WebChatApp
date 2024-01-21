from datetime import date
from typing import Literal

from fastapi import APIRouter

from backend.entities import (
    Chat,
    ChatCollection,
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("")
def get_users():
    pass

@chats_router.get("/{chat_id}")
def get_user(chat_id: str):
    pass


@chats_router.put("/{chat_id}")
def update_user(user_id: str):
    pass


@chats_router.delete("/{chat_id}")
def delete_user(chat_id: str):
    pass


@chats_router.get("/{chat_id}/messages")
def get_user_fosters(chat_id: str):
    pass

@chats_router.get("/{chat_id}/users")
def get_user_fosters(chat_id: str):
    pass