from datetime import date
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter

from backend.entities import(
    User,
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
@users_router.post("", response_model=User)
def create_user(user_create: UserCreate):
    """Creates a new user in the database if the ID doesn't match an already created user"""
    
    return db.create_user(user_create)


@users_router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    """Get a user for a given ID."""
    
    return db.get_user_by_id(user_id)

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(user_id: str):
    
    return db.get_user_chats(user_id)