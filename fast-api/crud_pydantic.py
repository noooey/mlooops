from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define input schema
class CreateIn(BaseModel):
    name: str
    nickname: str

# Define output schema
class CreateOut(BaseModel):
    status: str
    id: int

# create a FastAPI Instance
app = FastAPI()

# User db
USER_DB = {}

# Fail response
NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found.")

# api 
@app.post("/users", response_model=CreateOut)
def create_user(user: CreateIn) -> CreateOut:
    USER_DB[user.name] = user.nickname
    return CreateOut(status="success", id=len(USER_DB))

@app.get("/users")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname": USER_DB[name]}

@app.put("/users")
def update_user(name: str, nickname: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}

@app.delete("/users")
def delete_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status": "success"}