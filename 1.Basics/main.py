from fastapi import FastAPI
from pydantic import BaseModel

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


''' request body '''


@app.post("/items")
async def write_items(item: Item):
    fake_items.append(item.model_dump())
    return {"msg": "item added successfully", **item.model_dump()}
