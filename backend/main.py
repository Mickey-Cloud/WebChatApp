from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from backend.auth import auth_router, DuplicateValueException
from backend.routers.chats import chats_router
from backend.routers.users import users_router
from backend.database import (
    EntityNotFoundException,
    DuplicateEntityException,
)

from backend.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express API",
    description="API for managing users and chats.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )

@app.exception_handler(DuplicateEntityException)
def handle_duplicate_entity(
    _request: Request,
    exception: DuplicateEntityException,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_entity",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )
@app.exception_handler(DuplicateValueException)
def handle_duplicate_value(
    _request: Request,
    exception: DuplicateValueException
)-> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_value",
                "entity_name": exception.entity_name,
                "entity_field": exception.entity_field,
                "entity_value": exception.entity_value,
            },
        },
    )

@app.get("/", include_in_schema=False)
def default() -> str:
    return HTMLResponse(
        content=f"""
        <html>
            <body>
                <h1>{app.title}</h1>
                <p>{app.description}</p>
                <h2>API docs</h2>
                <ul>
                    <li><a href="/docs">Swagger</a></li>
                    <li><a href="/redoc">ReDoc</a></li>
                </ul>
            </body>
        </html>
        """,
    )