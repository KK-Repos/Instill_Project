import uvicorn
from app.config import HOST_PORT
from app.main import app


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(HOST_PORT), reload=True)