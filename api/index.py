# api/index.py

from app.main import app

def handler(request):
    return app(request)
