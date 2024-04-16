from datetime import datetime

from fastapi import HTTPException

from sqlmodel import Session, SQLModel, create_engine, select

from backend.helpers import(
    from_MessagesInDB_to_Messages,
    messageInDB_to_Message,
)

from backend.schema import (
    UserInDB,
    UserRegistration,
    UserUpdate,
    UserChatLinkInDB,
    UserCollection,
    Chat,
    ChatInDB,
    ChatUpdate,
    ChatCollection,
    ChatResponseSm,
    MessageInDB,
    Message,
    
)

engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

class PermissionException(HTTPException):
    def __init__(self, status_code: int, error: str, description: str):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "error_description": description,
            },
        )

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
class NoPermissionChat(PermissionException):
    def __init__(self):
        super().__init__(
            status_code=403,
            error="no_permission",
            description="requires permission to edit chat"
        )
        
class NoPermissionChatMembers(PermissionException):
    def __init__(self):
        super().__init__(
            status_code=403,
            error="no_permission",
            description="requires permission to edit chat members"
        )

class InvalidState(PermissionException):
    def __init__(self):
        super().__init__(
            status_code=422,
            error="invalid_state",
            description="owner of a chat cannot be removed"
        )
        
#   -------- users --------   #


def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return session.exec(select(UserInDB)).all()

def update_user(session: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    """
    Update the username or email for a user

    Args:
        session (Session): database session
        user_id (int): user's id
        user_update (UserUpdate): Information to update on the user

    Returns:
        UserInDB: The updated user
    """
    
    user = get_user_by_id(session, user_id)
    for key, value in user_update:
        if(value != None):
            setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def get_user_chats(session: Session, user_id: int) -> ChatCollection:
    """
    Retrieves a collection of chats the user has participated in
    
    :param user_id: id of the user whose chats we want
    :return: collection of the chats
    :raise: EntityNotFoundException if the user's id is not found
    """
    
    user = get_user_by_id(session, user_id)
    
    chat_list = get_chats(session)
    
    return [chat for chat in chat_list if user in chat.users]

# ----------------- Chats --------------------- #

def get_chats(session: Session) -> ChatCollection:
    """
    Retrieves a list of all the chats
    
    Returns:
        ChatCollection: a chat collection in the chat response format
    """
    return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
    """
    Retrieve an chat from the database.
    
    :param chat_id: id of the chat to be retrieved
    :return: the retrieved chat
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def post_new_chat(session: Session, name: str, owner_id: int)-> ChatResponseSm:
    """Creates a new chat

    Args:
        session (Session): database session

    Returns:
        ChatResponseSm: The created chat
    """
    
    newChat = ChatInDB(
        name=name,
        owner_id=owner_id
    )
    session.add(newChat)
    session.commit()
    session.refresh(newChat)
    nChat = Chat(
        id=newChat.id,
        name=newChat.name,
        owner=newChat.owner,
        created_at=newChat.created_at
        )
    return ChatResponseSm(chat=nChat)

def put_chat_name_update(session: Session, chat_id: int, owner_id: int, chat_update: ChatUpdate) -> Chat:
    """
    Update the Name of a Chat

    Args:
        chat_id (str): the chat to be updated
        chat_update (ChatUpdate): the name to update in the chat
    """
    chat = get_chat_by_id(session, chat_id)
    if(chat.id != owner_id):
        raise NoPermissionChat()
    for key, value in chat_update:
        setattr(chat, key, value)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    
    return Chat(
        id=chat.id,
        name=chat.name,
        owner=chat.owner,
        created_at=chat.created_at
    )

def delete_chat(session: Session, chat_id: int):
    """
    Deletes a chat based off the given ID

    Args:
        chat_id (str): ID of the chat to be deleted
    Raises:
        Entity Not found exception if
    """
    
    chat = get_chat_by_id(session, chat_id)
    session.delete(chat)
    session.commit()

def get_messages_by_chat_id(session: Session, chat_id: int) -> list[Message]:
    """
    Get all the messages for a given chat ID

    Args:
        chat_id (str): The ID of the Chat to receive the messages for
    """
    
    chat = get_chat_by_id(session, chat_id)
    messages = from_MessagesInDB_to_Messages(chat.messages)
    return messages

def get_chat_users(session: Session, chat_id: int) -> list[UserInDB]:
    """
    Get all the users associated with the particular chat

    Args:
        chat_id (str): Id of the chat to get the user data for
    Raise:
        404 EntityNotFoundException if the given chat is not found
    """
    
    chat = get_chat_by_id(session, chat_id)
    
    users = chat.users
    return users

def put_new_chat_user(session: Session, chat_id: int, user_id: int, owner_id:int) -> UserCollection:
    """Puts a new user in a chat

    Args:
        chat_id (int): Id of the chat to add the user to
        user_id (int): Id of the user to add to the chat
        owner_id (int): Id of the owner of the chat

    Returns:
        UserCollection: A list of all the users that belong to the chat
    """
    chat = get_chat_by_id(session,chat_id)
    if(chat.id != owner_id):
        raise NoPermissionChatMembers()
    get_user_by_id(session,user_id)
    result = session.exec(select(UserChatLinkInDB).where(UserChatLinkInDB.user_id == user_id).where(chat_id))
    if(result is not None):
        usersInChat = get_chat_users(session, chat_id)
        return UserCollection(
            meta=usersInChat.count(),
            users=usersInChat
            )
    link = UserChatLinkInDB(user_id, chat_id)
    session.add(link)
    session.commit()
    session.refresh(link)
    usersInChat = get_chat_users(session, chat_id)
    return UserCollection(
        meta=usersInChat.count(),
        users=usersInChat
        )
    
def delete_user_chat_link(session: Session, chat_id: int, user_id: int, owner_id: int) -> UserCollection:
    """Removea a user from a chat

    Args:
        chat_id (int): id of the chat to remove the user from
        user_id (int): id of the user to be removed from the chat
        owner_id (int): id of the owner of the chat

    Returns:
        UserCollection: a collection of all the users left in the chat
    """
    chat = get_chat_by_id(session,chat_id)
    if(chat.id != owner_id):
        raise NoPermissionChatMembers()
    if(user_id == owner_id):
        raise InvalidState()
    get_user_by_id(session,user_id)
    result = session.exec(select(UserChatLinkInDB).where(UserChatLinkInDB.user_id == user_id).where(chat_id))
    if(result is not None):
        usersInChat = get_chat_users(session, chat_id)
        return UserCollection(
            meta=usersInChat.count(),
            users=usersInChat
            )
    link = UserChatLinkInDB(user_id, chat_id)
    session.add(link)
    session.commit()
    session.refresh(link)
    usersInChat = get_chat_users(session, chat_id)
    return UserCollection(
        meta=usersInChat.count(),
        users=usersInChat
        )
    

def post_message(session: Session, chat_id: int, user_id: int, text: str) -> MessageInDB:
    """
    Post a new message to a chat

    Args:
        session (Session): database session
        chat_id (int): id of the chat to add the message to
        user_id (int): user adding the message
        text (str): text of the message added

    Returns:
        MessageInDB: database version of the message added
        
    Raises:
        EntityNotFound: The chat to add the message to does not exist.
    """
    get_chat_by_id(session, chat_id)
    message = MessageInDB(
        text=text,
        user_id=user_id,
        chat_id=chat_id
    )
    
    session.add(message)
    session.commit()
    session.refresh(message)
    
    return messageInDB_to_Message(message)