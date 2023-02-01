#Bakcend con fastapi
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

"""user classs"""
class User(BaseModel):
    
    id:int
    name:str
    surname:str
    url:str
    age:int

users_list = [User(id=1,name="pepe",surname="problemas",url="www.pepeproblemas.com",age=30),
             User(id= 2,name="mariano",surname="matamoros",url="www.matamoros.com",age=30),
             User(id= 3,name="aragón",surname="Galván",url="www.aragongalvan.com",age=30)]

@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")
async def user(id:int):
    return SearchUser(id)
    
    
@app.get("/userquery/")
async def user(id:int):
    return SearchUser(id)

@app.post("/user/")
async def user(user:User):
    if type( SearchUser(user.id)) == User:
        return {"error":"el usuario ya existe"}
    else:
        users_list.append(user)
    
    
    
    
def SearchUser(id):
    usrs = filter(lambda User: User.id == id, users_list )
    try:
        return list(usrs)[0]
    except:
        return '{"error":"no se ha encontrado el usuario"}'
    