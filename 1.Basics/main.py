from fastapi import FastAPI, status, Query, Path, Cookie, Header, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Annotated
from fastapi.staticfiles import StaticFiles

app = FastAPI()

fake_items = [
    {"name": "Apples", "item_id": 1},
    {"name": "Bananas", "item_id": 2},
    {"name": "Mangoes", "item_id": 3},
]


class Item(BaseModel):
    name: str
    item_id: int


@app.get("/")
async def root():
    return {"message": "Hello Mom!"}


''' path params '''


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


''' query params '''


@app.get("/items")
async def read_items(skip: int = 0, limit: int = 0, search: str | None = None):
    return {"items": fake_items[skip:skip + limit], "search": search}


''' request body & status codes'''


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def write_items(item: Item):
    fake_items.append(item.model_dump())
    return {"msg": "item added successfully", **item.model_dump()}


''' Query Params and String validations '''


@app.get("/users")
async def read_users(q: Annotated[str | None, Query(max_length=10)] = None):
    users = {"users": [{"name": "sharath"}, {"name": "mohan"}]}
    if q:
        users.update({"q": q})
    return users


@app.get("/users/me")
async def read_users_me(q: Annotated[str, Query(title="search query", max_length=10)] = "Ricky",
                        qlist: Annotated[list[str] | None, Query()] = None):
    users = {"users": [{"name": "sharath"}, {"name": "mohan"}]}
    if q:
        users.update({"q": q})
    if qlist and len(qlist):
        users.update({"qlist": qlist})
    return users


''' Path Parameters and Numeric validations '''


@app.get("/users/{user_id}")
async def read_user_details(user_id: Annotated[int, Path(title="user id", ge=1)]):
    return {"user_id": user_id}


''' Cookies '''


@app.get("/cookies")
async def set_cookie(add_id: Annotated[str | None, Cookie()] = None):
    return {"add_id": add_id}


''' Headers '''


@app.get("/headers")
async def read_headers(authorization: Annotated[str | None, Header()] = None,
                       strange_header: Annotated[str | None, Header()] = None):
    return {"authorization": authorization, "strange_header": strange_header}


''' static files '''
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


'''files'''


@app.post("/file")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


''' upload files  '''


@app.post("/upload_file")
async def upload_file(file:Annotated[UploadFile, File()]):
    if file.content_type != 'image/png':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid file format")
    return {"file_size": file.size}