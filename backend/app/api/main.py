from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import users, accounts, positions, prices

app = FastAPI(
    title="Portana API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Allow requests from Nuxt/Vue dev server
origins = [
    "http://localhost:3000",
]

# ✅ Correct usage of CORS middleware
app.add_middleware(
    # type: ignore
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers with prefixes
app.include_router(users.router, prefix="/api/users")
app.include_router(accounts.router, prefix="/api/accounts")
app.include_router(positions.router, prefix="/api/positions")
app.include_router(prices.router, prefix="/api/prices")
