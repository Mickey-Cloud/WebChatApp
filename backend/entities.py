from datetime import date, datetime


from pydantic import BaseModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

# ---------------- Users -------------------- #
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

# -------------- Messages ----------- #
class Message(BaseModel):
    
    id: str
    user_id: str
    text: str 
    created_at: datetime
    
class MessageCollection(BaseModel):
    """Represents an API response for a collection of Messages"""
    
    meta: Metadata
    messages: list[Message]

# ------------- Chats -------------- #
class Chat(BaseModel):
    """Represents an API response for a chat."""

    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class ChatDB(BaseModel):
    id: str
    name: str
    messages: list[Message]
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    
    meta: Metadata
    chats: list[Chat]

class ChatUpdate(BaseModel):
    """Represents an API body for a chat update"""
    
    name: str

