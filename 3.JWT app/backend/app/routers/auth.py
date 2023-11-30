from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, and_
from passlib.hash import bcrypt
from ..models.user import User as DBUser
from ..database.main import engine

router = APIRouter()


class User(BaseModel):
    name: str
    email: str
    password: str


class SignInUser(BaseModel):
    email: str
    password: str


def hash_password(password: str):
    return bcrypt.hash(password)


@router.post("/signup", tags=["auth", "signup"])
async def register_user(user: User):
    hashed_password = hash_password(user.password)
    new_user = DBUser(name=user.name, email=user.email, password=hashed_password)
    try:
        with Session(engine) as session:
            session.add(new_user)
            session.commit()
            return {"message": "Registered successfully"}
    except IntegrityError as e:
        if 'UNIQUE constraint failed: user.email' in str(e.__cause__):
            raise HTTPException(status_code=400, detail="User already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin", tags=["auth", "signin"])
async def signin_user(user: SignInUser):
    hashed_password = hash_password(user.password)
    with Session(engine) as session:
        # statement = select(DBUser).where(and_(DBUser.email == user.email, DBUser.password == hashed_password))
        statement = select(DBUser).where(DBUser.email == user.email)
        results = session.exec(statement)
        session.close()
        for data in results:
            print(bcrypt.verify(user.password, data.password))
        if not results:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return {"message": "successfully loggedIn"}
