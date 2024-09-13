from ninja import Schema
from pydantic import EmailStr, Field


class LoginRequest(Schema):
    email: EmailStr
    password: str = Field(..., min_length=8)
