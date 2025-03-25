from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import random

# Secret key for JWT (Change this in production)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if frontend runs on a different port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

def create_jwt_token(username: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": username, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        token = create_jwt_token(request.username)
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="token", value=token, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    lucky_number = random.randint(1, 100)
    return {"message": f"Welcome, {user}! Your lucky number is {lucky_number}"}

@app.post("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("token")
    return response
