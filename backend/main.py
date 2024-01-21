from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

from backend.routers.chats import chats_router
from backend.routers.users import users_router

app = FastAPI(
    title="Pony Express API",
    description="API for managing users and chats.",
    version="0.1.0",
)

app.include_router(chats_router)
app.include_router(users_router)


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