#Bakcend con fastapi
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router=APIRouter()

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

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id:int):
    return SearchUser(id)
    
    
@router.get("/userquery/")
async def user(id:int):
    return SearchUser(id)

@router.post("/user/",status_code=201)
async def user(user:User):
    if type( SearchUser(user.id)) == User:
        raise HTTPException(status_code=404,detail="el usuario ya existe")
    
    users_list.append(user)
    return user
  
  
@router.put("/user/")
async def user(user:User):
    
    found = False
    
    for i,saved_user in enumerate( users_list):
        if saved_user.id == user.id:
            users_list[i]=user
            found = True
            
    if not found:
        return {"error":"no se ha actualizado el usuario"}

    return user
    

@router.delete("/user/{id}")
async def user(id:int):
    found = False
    
    for i,saved_user in enumerate( users_list):
        if saved_user.id == id:
            del users_list[i]
            found = True
            
    if not found:
        return {"error":"el usuario no existe"}

def SearchUser(id):
    usrs = filter(lambda User: User.id == id, users_list )
    try:
        return list(usrs)[0]
    except:
        
        return {"error":"no se ha encontrado el usuario"}
    