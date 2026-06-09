from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt

from app.models import LoginRequest, TokenResponse, RefreshRequest, UserInfo
from app.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_SECONDS,
)

app = FastAPI(
    title="FastAPI JWT Authentication",
    description="Web API con autenticación JWT implementada con FastAPI",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    if not authenticate_user(request.usuario, request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": request.usuario})
    refresh_token = create_refresh_token({"sub": request.usuario})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_token=refresh_token,
    )


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest):
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        usuario = payload.get("sub")
        if not usuario:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token({"sub": usuario})
    new_refresh_token = create_refresh_token({"sub": usuario})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_token=new_refresh_token,
    )


@app.get("/api/me", response_model=UserInfo)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        usuario = payload.get("sub")
        if not usuario:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return UserInfo(usuario=usuario)
