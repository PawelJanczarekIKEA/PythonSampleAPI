from typing import Union
import nest_asyncio
import azure.functions as func
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from FastAPIApp import app  # Main API application

nest_asyncio.apply()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


items = {
    '1': {'name': "Item 1", "price": 10.10, "is_offer": None},
    '2': {'name': "Item 2", "price": 20.20, "is_offer": True},
    '3': {'name': "Item 3", "price": 20.20, "is_offer": False},
}


# GET
@app.get("/")
async def root():
    return {'message': "Hello World"}


@app.get("/hello/")
async def say_hello_no_name():
    return {'message': f"Hello noname"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {'message': f"Hello {name}"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}


# POST
@app.post("/items/")
async def create_item(item: Item):
    return item


# PATCH
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


# PUT
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {'message': f"Item {item_id} deleted."}


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
