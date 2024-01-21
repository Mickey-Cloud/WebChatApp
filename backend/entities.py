from datetime import date, datetime

from pydantic import BaseModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

class User(BaseModel):
    """Represents an API response for a user."""

    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system"""

    id: str

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]

class Chat(BaseModel):
    """Represents an API response for a chat."""

    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    
    meta: Metadata
    chats: list[Chat]
