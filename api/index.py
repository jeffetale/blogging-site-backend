# api/index.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append(".")

from app.main import app as fastapi_app

app = fastapi_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

