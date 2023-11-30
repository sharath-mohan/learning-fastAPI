from fastapi import FastAPI
from sqlmodel import SQLModel
from .routers import auth
from .database.main import engine
from .models.user import User

app = FastAPI()

app.include_router(auth.router, prefix="/auth")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    print("start up")
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Hello from fast API"}
