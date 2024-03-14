import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db
from backend import auth
from backend.schema import *

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()
    
@pytest.fixture
def logged_in_client(session, user_fixture):
    def _get_session_override():
        return session

    def _get_current_user_override():
        return user_fixture(username="miguel",
                            email="migi@test.test",
                            password="miguelpassword")

    app.dependency_overrides[db.get_session] = _get_session_override
    app.dependency_overrides[auth.get_current_user] = _get_current_user_override

    yield TestClient(app)

    app.dependency_overrides.clear()
    
@pytest.fixture
def user_fixture(session):
    def _build_user(
        username: str = "miguel",
        email: str = "migi@test.test",
        password: str = "miguelpassword",
    )-> db.UserInDB:
        return auth.register_new_user(
            auth.UserRegistration(
                username=username,
                email=email,
                password=password,
            ),
            session,
        )
    return _build_user

@pytest.fixture
def default_users():
    return[
        UserInDB(
            id=1,
            username="richard",
            email="richard@test.com",
            hashed_password="richard123",
            created_at= datetime.now()
        ), UserInDB(
            id=2,
            username="mickey",
            email="mickey@test.com",
            hashed_password="mickey123",
            created_at= datetime.now()
        ), UserInDB(
            id=3,
            username="loose",
            email="loose@test.com",
            hashed_password="loose123",
            created_at= datetime.now()
        ),
    ]

@pytest.fixture
def default_chats():
    return[
        ChatInDB(
            id=1,
            name= "Mikes Chat",
            owner_id= 1,
            created_at= datetime.now()
        ),
        ChatInDB(
            id=2,
            name= "Stevens Chat",
            owner_id= 3,
            created_at= datetime.now()
        ),
        ChatInDB(
            id=3,
            name= "Louis Chat",
            owner_id= 3,
            created_at= datetime.now()
        ),
        
    ]

@pytest.fixture
def default_messages():
    return[
        MessageInDB(
            id=1,
            text="you are testy",
            user_id= 1,
            chat_id=1,
            created_at= datetime(2018,1,1,12,1,2),
        ),
        MessageInDB(
            id=2,
            text="you are zesty",
            user_id= 2,
            chat_id=1,
            created_at= datetime(2018,1,2,12,1,2),
        ),
        MessageInDB(
            id=3,
            text="you are tasty",
            user_id= 1,
            chat_id=1,
            created_at= datetime(2018,1,3,12,1,2),
        ),
        MessageInDB(
            id=4,
            text="you are Qesty",
            user_id= 2,
            chat_id=1,
            created_at= datetime(2018,1,4,12,1,2),
        ),
        MessageInDB(
            id=5,
            text="you are testy",
            user_id= 3,
            chat_id=2,
            created_at= datetime(2019,1,1,12,1,2),
        ),
        MessageInDB(
            id=6,
            text="you are the sexiest person alive",
            user_id= 1,
            chat_id=2,
            created_at= datetime(2019,1,1,12,2,2),
        ),
        MessageInDB(
            id=7,
            text="Thank you I know it",
            user_id= 3,
            chat_id=2,
            created_at= datetime(2019,1,1,12,3,2),
        ),
        MessageInDB(
            id=8,
            text="and the humblest",
            user_id= 1,
            chat_id=2,
            created_at= datetime(2019,1,1,12,4,2),
        ),
        MessageInDB(
            id=9,
            text="you said it not me",
            user_id= 3,
            chat_id=2,
            created_at= datetime(2019,1,1,12,5,2),
        ),
        MessageInDB(
            id=10,
            text="***sigh*** yeah you're not wrong lol",
            user_id= 1,
            chat_id=2,
            created_at= datetime(2019,1,1,12,6,2),
        ),
        MessageInDB(
            id=11,
            text="I am alone",
            user_id= 3,
            chat_id=3,
            created_at= datetime(2023,1,1,12,1,2),
        ),
    ]

@pytest.fixture
def default_user_chat_links():
    return [
        UserChatLinkInDB(
            user_id=1,
            chat_id=1,
        ),
        UserChatLinkInDB(
            user_id=2,
            chat_id=1,
        ),
        UserChatLinkInDB(
            user_id=1,
            chat_id=2,
        ),
        UserChatLinkInDB(
            user_id=3,
            chat_id=2,
        ),
        UserChatLinkInDB(
            user_id=3,
            chat_id=3,
        ),
    ]
    
@pytest.fixture
def default_database(session, default_chats, default_users, default_messages, default_user_chat_links):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.add_all(default_messages)
    session.add_all(default_user_chat_links)
    session.commit()