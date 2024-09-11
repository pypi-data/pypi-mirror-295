import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: Optional[EmailStr]
    sub: uuid.UUID
    roles: list[str]

    class Config:
        from_attributes = True
