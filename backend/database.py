import json
from datetime import date, datetime

from backend.entities import (
    Chat,
    User,
    UserCreate,
    ChatCollection,
    ChatUpdate,
    ChatDB,
    Message,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- users --------   #


def get_all_users() -> list[User]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [User(**user_data) for user_data in DB["users"].values()]


def create_user(user_create: UserCreate) -> User:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    :raise: DuplicateEntityException if the user id already exists
    """

    user = User(
        created_at=datetime.today(),
        **user_create.model_dump(),
    )
    if user.id not in DB["users"]:
        DB["users"][user.id] = user.model_dump()
        return user
    
    raise DuplicateEntityException(entity_name="User", entity_id=user.id)


def get_user_by_id(user_id: str) -> User:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    if user_id in DB["users"]:
        return User(**DB["users"][user_id])

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def get_user_chats(user_id: str) -> ChatCollection:
    """
    Retrieves a collection of chats the user has participated in
    
    :param user_id: id of the user whose chats we want
    :return: collection of the chats
    :raise: EntityNotFoundException if the user's id is not found
    """
    
    if user_id not in DB["users"]:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    
    chat_list = get_chats()
    
    return [chat for chat in chat_list if user_id in chat.user_ids]

# ----------------- Chats --------------------- #

def get_chats() -> ChatCollection:
    """
    Retrieves a list of all the chats
    
    Returns:
        ChatCollection: _description_
    """
    return [Chat(**chat_data) for chat_data in DB["chats"].values()]

def get_chat_by_id(chat_id: str) -> Chat:
    """
    Retrieve an chat from the database.
    
    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    if chat_id in DB["chats"]:
        return Chat(**DB["chats"][chat_id])

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def put_chat_name_update(chat_id: str, chat_update: ChatUpdate) -> Chat:
    """
    Update the Name of a Chat

    Args:
        chat_id (str): the chat to be updated
        chat_update (ChatUpdate): the name to update in the chat
    """
    chat = get_chat_by_id(chat_id)
    
    updated_chat = Chat(
        **{
        **chat.model_dump(),
        **chat_update.model_dump()
        }
    )
    DB["chats"][chat_id] = updated_chat.model_dump()
    
    return updated_chat

def delete_chat(chat_id: str):
    """
    Deletes a chat based off the given ID

    Args:
        chat_id (str): ID of the chat to be deleted
    Raises:
        Entity Not found exception if
    """
    
    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]

def get_messages_by_chat_id(chat_id: str) -> list[Message]:
    """
    Get all the messages for a given chat ID

    Args:
        chat_id (str): The ID of the Chat to receive the messages for
    """
    if chat_id not in DB["chats"]:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    
    chat = ChatDB(**DB["chats"][chat_id])
    return chat.messages

def get_chat_users(chat_id: str) -> list[User]:
    """
    Get all the users associated with the particular chat

    Args:
        chat_id (str): Id of the chat to get the user data for
    Raise:
        404 EntityNotFoundException if the given chat is not found
    """
    
    chat = get_chat_by_id(chat_id)
    
    users = list()
    for userId in chat.user_ids:
        users.append(get_user_by_id(userId))
    
    return users