from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username :str
    full_name:str
    email    :str
    disabled :bool
    
class UserDB(User):
    password :str

users_db = {
    "mouredev" : {
        "username" :"mouredev",
        "full_name":"Brais Moure",
        "email"    :"braismoure@mouredev.com",
        "disabled" : False,
        "password" : "qwerty"
    },
    "quetzihack" : {
        "username" :"QuetziHack",
        "full_name":"Chinji Okumura",
        "email"    :"ching@oku.com",
        "disabled" : False,
        "password" : "fghjkl"
    }
}

def searchUserDB(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def searchUser(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token :str = Depends(oauth2)):
    user = searchUser(token)
    
    if not user:
        raise HTTPException(status_code=401,
                            detail="Credenciales invalidas",
                            headers={"WWW-Authenticate":"Bearer"})
        
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,detail="Usuario inactivo")
    
    return user
    
    
@app.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends()):
    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El ususario no es correcto")
    
    user = searchUserDB(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400,detail="Contraseña incorrecta")
    
    return {"access_token":user.username, "token_type" : "Bearer"}


@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user