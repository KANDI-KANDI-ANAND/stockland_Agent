import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import chat_routes

app = FastAPI(
    title="Stockland AI Agent",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("reports"):
    os.makedirs("reports")

app.include_router(
    chat_routes.router,
    prefix="/api",
    tags=["Chat"]
)

app.mount("/reports", StaticFiles(directory="reports"), name="reports")
