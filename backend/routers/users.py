from datetime import date
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter

from backend.entities import(
    User,
    UserResponse,
    UserCreate,
    UserCollection,
    ChatCollection
)
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(
    sort: Literal["id", "created_at"] = "id",
):
    """Get a collection of users."""

    sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users()

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

#need to add duplicate entity option
@users_router.post("", response_model=UserResponse)
def create_user(user_create: UserCreate):
    """Creates a new user in the database if the ID doesn't match an already created user"""
    
    return UserResponse(
        user=db.create_user(user_create))


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get a user for a given ID."""
    
    return UserResponse(
        user=db.get_user_by_id(user_id))

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(
    user_id: str,
    sort: Literal["name", "id", "created_at"] = "name"
    ):
    """Gets all the chats pertaining to a specific user"""
    
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_user_chats(user_id)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )