from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

users = [{"user_id": 1, "name": "Naruto"}]


class User(BaseModel):
    user_id: int
    name: str


@router.get("/users/", tags=["users"])
async def read_users():
    return {"users": users}


@router.post("/users/", status_code=status.HTTP_201_CREATED, tags=["users"])
async def write_users(user: User):
    users.append(user.model_dump())
    return {"message": "User added successfully", **user.model_dump()}
