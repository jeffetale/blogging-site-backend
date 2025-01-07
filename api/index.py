# api/index.py

from fastapi import FastAPI, Request
from app.main import app
from mangum import Mangum

handler = Mangum(app, lifespan="off")
