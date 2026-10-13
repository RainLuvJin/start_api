from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4


app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    is_offer : bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "Item": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, Item: Item):
    return {"item_id": item_id, "item_name": Item.name, "item_price": Item.price}

@app.post("/items/{item_id}")
def read_item(item_id: int, Item: Item):
    return {"item_id": item_id, "Item": Item}

@app.get("/hello")
def say_hello():
    return {"message":"Hello, Jinny!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            404,
            "User not found",
        )
    return {"user_id":user_id, "name":"Jinny"}


sessions = {}

class session(BaseModel):
    username : str
    info : str

@app.post("/sessions")
def create_session(data: session):
    session_id = str(uuid4())
    # problem: 我不会生成sessioniD，只会传参。
    如果字典里sessioniD是唯一的：
        sessions[session_id] = {"username":data.username,"info":data.info}
    如果不唯一：
        return("sessionid已存在，请重新键入")
    return {"session_id": session_id, "status":"created"}

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    if id不存在：
        raise HTTPException(
            404,
            "id not found"
        )
    return {"session_id": session_id, "username":sessions[session_id]["username"],"info":sessions[session_id]["info"]}

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    sessions[session_id] = None
    return {"session_id": session_id, "status":"deleted"}