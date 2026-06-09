from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    usuario: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 300


class RefreshRequest(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    usuario: str
    id: Optional[int] = None
