import os
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, SQLModel, select

from backend import database as db
from backend.schema import (
    User, 
    UserInDB,
    UserResponse,
    Claims,
    UserRegistration,
    AccessToken
    )

class DuplicateValueException(Exception):
    def __init__(self, *, entity_name: str, entity_field: str, entity_value: str):
        self.entity_name = entity_name
        self.entity_field = entity_field
        self.entity_value = entity_value

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_key = os.environ.get("JWT_KEY", default="insecure-jwt-key-for-dev")
jwt_alg = "HS256"

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

class AuthException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=401,
            detail={
                "error": error,
                "error_description": description,
            },
        )

class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid username or password",
        )

class InvalidToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid access token",
        )

class ExpiredToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="expired access token",
        )

def get_current_user(
    session: Session = Depends(db.get_session),
    token: str = Depends(oauth2_scheme),
) -> UserInDB:
    """FastAPI dependency to get current user from bearer token."""
    user = _decode_access_token(session, token)
    return user


@auth_router.post("/registration", response_model=UserResponse)
def register_new_user(
    registration: UserRegistration,
    session: Annotated[Session, Depends(db.get_session)],
):
    """Register new user."""

    duplicateUser = session.exec(select(UserInDB).where(UserInDB.username == registration.username)).first()
    if(duplicateUser != None):
        raise DuplicateValueException(entity_name="User", entity_field="username", entity_value=registration.username)
    duplicateUser = session.exec(select(UserInDB).where(UserInDB.email == registration.email)).first()
    if(duplicateUser != None):
        raise DuplicateValueException(entity_name="User", entity_field="email", entity_value=registration.email)
    
    hashed_password = pwd_context.hash(registration.password)
    user = UserInDB(
        **registration.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user = user)


@auth_router.post("/token", response_model=AccessToken)
def get_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session),
):
    """Get access token for user."""

    user = _get_authenticated_user(session, form)
    return _build_access_token(user)


def _get_authenticated_user(
    session: Session,
    form: OAuth2PasswordRequestForm,
) -> UserInDB:
    user = session.exec(
        select(UserInDB).where(UserInDB.username == form.username)
    ).first()

    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()

    return user


def _build_access_token(user: UserInDB) -> AccessToken:
    expiration = int(datetime.now(timezone.utc).timestamp()) + access_token_duration
    claims = Claims(sub=str(user.id), exp=expiration)
    access_token = jwt.encode(claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )


def _decode_access_token(session: Session, token: str) -> UserInDB:
    try:
        claims_dict = jwt.decode(token, key=jwt_key, algorithms=[jwt_alg])
        claims = Claims(**claims_dict)
        user_id = claims.sub
        user = session.get(UserInDB, user_id)

        if user is None:
            raise InvalidToken()

        return user
    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        raise InvalidToken()
    except ValidationError():
        raise InvalidToken()