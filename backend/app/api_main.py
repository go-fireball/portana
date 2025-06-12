from fastapi import FastAPI
from app.api.routes import users

app = FastAPI(title="Portana API")

app.include_router(users.router, prefix="/api/users")
