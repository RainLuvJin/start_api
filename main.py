from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

# 问题1：如何由后端生成用户id？
from uuid import uuid4
sessions = {}
# 问题2：Python的类名通常采用PascalCase大驼峰命名法。
class SessionCreateRequest(BaseModel):
    username : str
    info : str

@app.post("/sessions")
def create_session(data: SessionCreateRequest):
    session_id = str(uuid4())
    sessions[session_id] = {"username":data.username,"info":data.info}
    return {"session_id": session_id, "status":"created"}

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    # 问题3：如果x不在一个集合里if x not in list:
    if session_id not in sessions:
        raise HTTPException(
            404,
            "Session not found"
        )
    # 问题4：pydantic类模型使用属性才用. 比如data.username；字典里索引key用[]
    # 问题5：可以直接返回保存了完整记录的字典
    else:
        return sessions[session_id]

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(
            404,
            "Session not found"
        )
        # 问题6：如何删除字典一条值
    sessions.pop(session_id)
    return {"session_id": session_id, "status":"deleted"}