from fastapi import FastAPI
from app.api.routes import users, accounts, positions

app = FastAPI(
    title="Portana API",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
    openapi_url="/openapi.json"  # Raw schema
)

app.include_router(users.router, prefix="/api/users")
app.include_router(accounts.router, prefix="/api/accounts")
app.include_router(positions.router, prefix="/api/positions")
