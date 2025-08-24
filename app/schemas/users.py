from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    nombres: str = Field(min_length=3, max_length=80)
    apellidos: str = Field(min_length=3, max_length=80)
    identificacion: str = Field(min_length=6, max_length=12)
    id_rol: int
    correo: EmailStr
    telefono: str = Field(min_length=7, max_length=15)
    estado: bool


class UserCreate(UserBase):
    pass_hash: str = Field(min_length=8)

class UserUpdate(BaseModel):
    nombres: Optional[str] = Field(default=None, min_length=3, max_length=80)
    apellidos: Optional[str] = Field(default=None, min_length=3, max_length=80)
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=15)
    estado: Optional[bool] = None
    correo: Optional[EmailStr]= Field(default=None, min_length=7, max_length=100)
class UserOut(UserBase):
    id_usuario: int