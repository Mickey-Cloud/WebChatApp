from datetime import date
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.auth import get_current_user

from backend.schema import(
    UserCollection,
    UserResponse,
    UserInDB,
    UserUpdate,
    ChatCollection,
)
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(
    sort: Literal["id", "created_at"] = "id",
    session: Session = Depends(db.get_session)
):
    """Get a collection of users."""

    sort_key = lambda user: getattr(user, sort)
    users = db.get_all_users(session)

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@users_router.get("/me", response_model=UserResponse)
def get_me(
    user: UserInDB = Depends(get_current_user)
    ):
    """Get Current User"""
    return UserResponse(user=user)

@users_router.put("/me", response_model=UserResponse)
def update_me(
    update_user: UserUpdate,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
    ):
    """Updates the username or email for the logged in user"""
    return UserResponse(user=db.update_user(session, user.id, update_user))

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(db.get_session)
    ):
    """Get a user for a given ID."""
    
    return UserResponse(
        user=db.get_user_by_id(session, user_id))

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(
    user_id: int,
    sort: Literal["name", "id", "created_at"] = "name",
    session: Session = Depends(db.get_session)
    ):
    """Gets all the chats pertaining to a specific user"""
    
    sort_key = lambda chat: getattr(chat, sort)
    chats = db.get_user_chats(session, user_id)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )