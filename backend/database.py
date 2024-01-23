import json
from datetime import date, datetime
from uuid import uuid4

from backend.entities import (
    Chat,
    User,
    UserCreate,
    ChatCollection,
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
    
    return [Chat(**chat_data) for chat_data in DB["chats"].values()]

# ----------------- Chats --------------------- #

