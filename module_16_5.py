from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel                             #базовая модель дляудобногопредставления данных
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []                                                 #база данных

class User(BaseModel):                                  #каждое сообщение будет иметь:
    id: int = None                                      #номер пользователя
    username: str                                       #имя пользователя
    age: int                                            #возраст пользователя

@app.get("/")
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})   #обращение к шаблону,куда подставляем данные                                   #возвращаем нашу базу данных

@app.get(path="/user/{user_id}")                                                            #возвращает сообщение на запрос id
async def get_message(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]}) #проверяем есть ли такой индекс, если нет то отрабртаеv ошибку
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/user/{username}/{age}")
async def create_message(user: User) -> str:
    user.id = len(users)
    users.append(user)
    return f"User {user} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_message(user_id: int, username: str, age: int) -> str:
    try:
        for user_ in users:
            if user_.id == user_id:
                user_.username = username
                user_.age = age
                return f"User {user_.id} has been updated"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_message(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f"User {user_id} has been deleted"                          #если такое сообщение не нашлось,
    except IndexError:                                                     #то срабатывает исключение
        raise HTTPException(status_code=404, detail="User was not found")
