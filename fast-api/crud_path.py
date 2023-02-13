from fastapi import FastAPI, HTTPException

app = FastAPI()

# Fail response
NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found.")

# user db
USER_DB = {}

@app.post("/users/name/{name}/nickname/{nickname}")
def create_user(name: str, nickname: str):
    USER_DB[name] = nickname
    return {"status": "success"}

@app.get("/users/name/{name}")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname": USER_DB[name]}

@app.put("/users/name/{name}/nickname/{nickname}")
def edit_user(name: str, nickname: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}

@app.delete("/users/name/{name}")
def read_root(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status": "success"}