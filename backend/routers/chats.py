from datetime import date, datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from backend.helpers import (
    messageInDB_to_Message,
    from_MessagesInDB_to_Messages,
    chatInDB_to_chat,
    chatsInDB_to_chats
)

from backend.schema import(
    ChatCollection,
    ChatUpdate,
    ChatResponse,
    ChatResponseSm, 
    ChatMetadata, 
    Chat,  
    MessageCollection,
    MessageResponse,
    MessageNew,
    UserCollection,
    UserInDB
)

from backend.auth import get_current_user
from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", response_model=ChatCollection)
def get_chats(
    sort: Literal["name", "id", "created_at"] = "name",
    session: Session = Depends(db.get_session)
    ):
    """Gets all the chats"""
    
    sort_key = lambda chat: getattr(chat, sort)
    chatList = db.get_chats(session)
    chats = chatsInDB_to_chats(chatList=chatList)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )



@chats_router.get("/{chat_id}", response_model=ChatResponse, response_model_exclude_none=True)
def get_chat(
    chat_id: int,
    include: list[str] = Query(None),
    session: Session = Depends(db.get_session)
    ):
    """Get a chat for a given ID."""
    
    chat = db.get_chat_by_id(session, chat_id)
    if include != None :
        if(include.__contains__("messages")):
            messages = from_MessagesInDB_to_Messages(chat.messages)
        else:
            messages= None
        if(include.__contains__("users")):
            users = chat.users
        else:
            users = None
    else:
        chat = ChatResponse(
            meta= ChatMetadata(
                message_count= len(chat.messages),
                user_count= len(chat.users)
                ),
            chat = Chat(
                id=chat.id,
                name=chat.name,
                owner=chat.owner,
                created_at=chat.created_at
                )
            )
        return chat
        
    
    if (messages == None and users != None):
        chat = ChatResponse(
            meta= ChatMetadata(
                message_count= len(chat.messages),
                user_count= len(chat.users)
                ),
            chat = Chat(
                id=chat.id,
                name=chat.name,
                owner=chat.owner,
                created_at=chat.created_at
                ),
            users = users
            )
    elif users == None and messages != None:
        chat = ChatResponse(
            meta= ChatMetadata(
                message_count= len(chat.messages),
                user_count= len(chat.users)
                ),
            chat = Chat(
                id=chat.id,
                name=chat.name,
                owner=chat.owner,
                created_at=chat.created_at
                ),
            messages=messages
            )
    else:
        chat = ChatResponse(
            meta= ChatMetadata(
                message_count= len(chat.messages),
                user_count= len(chat.users)
                ),
            chat = Chat(
                id=chat.id,
                name=chat.name,
                owner=chat.owner,
                created_at=chat.created_at
                ),
            messages=messages,
            users=users
            )
    
    return chat

@chats_router.put("/{chat_id}", response_model=ChatResponseSm)
def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
    ):
    """Changes the name of the given chat"""
    
    return ChatResponseSm(chat = db.put_chat_name_update(session, chat_id, user.id, chat_update))

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
def get_users_in_chat(
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
    
@chats_router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=201)
def post_message_to_chat(
    new_message: MessageNew,
    chat_id: int,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
    ):
    """Adds a message to the chat by the currently logged in user"""
    
    return MessageResponse(message = db.post_message(session, chat_id, user.id, new_message.text))

@chats_router.post("", response_model=ChatResponseSm, status_code=201)
def post_create_chat(
    name: ChatUpdate,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
):
    """Adds a chat with the logged in user as the owner

    Args:
        name (str): The name of the added chat
    """
    return db.post_new_chat(session, name.name, user.id)

@chats_router.put("/{chat_id}/users/{user_id}", response_model=UserCollection, status_code=201)
def put_new_chat_user(
    chat_id: int,
    user_id: int,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
):
    """Adds a user to the specified chat

    Args:
        chat_id (int): The chat to add the user to
        user_id (int): the user to add to the chat
    """
    
    return db.put_new_chat_user(session, chat_id, user_id, user.id)

@chats_router.delete("/{chat_id}/users/{user_id}", response_model=UserCollection)
def delete_user_chat_link(
    chat_id: int,
    user_id: int,
    user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session)
):
    """Removes a User from a chat

    Args:
        chat_id (int): The chat to remove the user from
        user_id (int): The Id of the user to be removed from the chat
    """
    
    return db.delete_user_chat_link(session, chat_id, user_id, user.id)