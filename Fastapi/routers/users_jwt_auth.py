
from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext 
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "1b50836543744048eb01f96f0cd14f52057ab151516b381c5b1b80080b5509b9"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password" : "$2y$10$op7Is.RYrWVefGvPIbUr/Oq1T7Z6LTpBojo0aOIA928VRmvW4ZK6S"
    },
    "quetzihack" : {
        "username" :"QuetziHack",
        "full_name":"Chinji Okumura",
        "email"    :"ching@oku.com",
        "disabled" : False,
        "password" : "$2y$10$s46leYHolqEzdb6PCF0XjObjxb4a1d6qUMC0d4/O8BlK9TYE6/8jm"
    }
}

def searchUserDB(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def searchUser(username:str):
    if username in users_db:
        return User(**users_db[username])

@app.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends()):
    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="El ususario no es correcto")
    
    user = searchUserDB(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400,detail="Contraseña incorrecta")
    
    pre_access_token = {'sub':user.username, 
                        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
}

    
    return {"access_token":jwt.encode(pre_access_token,SECRET,algorithm=ALGORITHM), "token_type" : "Bearer"}
 
 
async def auth_user(token: str = Depends(oauth2)):
    if not user:
        raise HTTPException(status_code=401,
                            detail="Credenciales invalidas",
                            headers={"WWW-Authenticate":"Bearer"})    


async def current_user(user :User = Depends(auth_user)):
        
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,detail="Usuario inactivo")
    
    return user
 
@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user