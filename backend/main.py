from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from uuid import uuid4
from pydantic import BaseModel
from typing import Dict
import time
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Simulated session store (Use Redis in production)
SESSIONS: Dict[str, Dict] = {}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        session_id = str(uuid4())
        SESSIONS[session_id] = {"username": request.username, "expires": time.time() + 3600}
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    session = SESSIONS[session_id]
    if session["expires"] < time.time():
        del SESSIONS[session_id]
        raise HTTPException(status_code=401, detail="Session expired")

    return session["username"]

@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    # Usually you would do CRUD operations here
    lucky_number = random.randint(1, 100)
    return {"message": f"Welcome, {user}! Your lucky number is {lucky_number}"}

@app.post("/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("session_id")
    return response
