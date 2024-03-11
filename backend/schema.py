from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from pydantic import BaseModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )
    
class UserCreate(SQLModel):
    """Request model for adding a new user to the system"""
    
    username: str
    email: str
    hashed_password: str

class UserResponse(BaseModel):
    """API response for user."""

    user: UserInDB
    
class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[UserInDB]

class UserUpdate(SQLModel):
    """Request model for updating a user in the system."""
    username: str = None
    email: str = None
    password: str = None

class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")

class ChatResponse(BaseModel):
    chat: ChatInDB

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    
    meta: Metadata
    chats: list[ChatInDB]
    
class ChatUpdate(SQLModel):
    name: str = None

class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")

class MessageCollection(BaseModel):
    """Represents an API response for a collection of Messages"""
    
    meta: Metadata
    messages: list[MessageInDB]