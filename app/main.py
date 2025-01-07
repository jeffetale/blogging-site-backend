# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from . import models
from .database import engine
from .routers import blog, contact, users
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "https://-frontend-domain.vercel.app"  # frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


