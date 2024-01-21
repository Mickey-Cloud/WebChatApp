from datetime import date
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter

from backend.entities import(
    User,
    UserCreate,
    UserCollection,
)
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(
    sort: Literal["id", "created_at"] = "id",
):
    """Get a collection of users."""

    sort_key = lambda animal: getattr(animal, sort)
    animals = db.get_all_users()

    return UserCollection(
        meta={"count": len(animals)},
        animals=sorted(animals, key=sort_key),
    )

#need to add duplicate entity option
@users_router.post("", response_model=User)
def create_user():
    """Creates a new user in the database if the ID doesn't match an already created user"""

    user = UserCreate(
    id=uuid4().hex,
    )
    usr = db.create_user(user)
    return User(
        usr.model_dump()
    )


@users_router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    """Get a user for a given ID."""
    
    return db.get_user_by_id(user_id)

@users_router.get("/{user_id}/chats")
def get_user_chats(user_id: str):
    pass