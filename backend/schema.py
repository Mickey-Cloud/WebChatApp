from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from pydantic import BaseModel


class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

class ChatMetadata(BaseModel):
    """Represents metadata for a chat collection"""
    message_count: int
    user_count: int
    

########################### User Models ##########################################

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
    
class User(SQLModel):
    """Data model for user."""
    id: int
    username: str
    email: str
    created_at: datetime

class UserResponse(BaseModel):
    """API response for user."""

    user: User
    
class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[UserInDB]

class UserUpdate(BaseModel):
    """Request model for updating a user in the system."""
    username: Optional[str] = None
    email: Optional[str] = None
####################### Message Models ###########################
class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: "ChatInDB" = Relationship(back_populates="messages")
    
class MessageNew(SQLModel):
    text: str

class MessageCollection(BaseModel):
    """Represents an API response for a collection of Messages"""
    
    meta: Metadata
    messages: list[MessageInDB]
    
class Message(BaseModel):
    id: int
    text: str
    chat_id: int
    user: User
    created_at: datetime

######################### Chat Models ##########################
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

class Chat(BaseModel):
    id: int
    name: str
    owner: User
    created_at: datetime

class ChatResponse(SQLModel):
    
    meta: ChatMetadata
    chat: Chat
    messages: Optional[list["Message"]] = None
    users: Optional[list[User]] = None

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""
    
    meta: Metadata
    chats: list[ChatInDB]

class ChatUpdate(SQLModel):
    name: str = None
    
#################### Auth Models #############################
class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str


class AccessToken(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str
    expires_in: int


class Claims(BaseModel):
    """Access token claims (aka payload)."""

    sub: str  # id of user
    exp: int  # unix timestamp