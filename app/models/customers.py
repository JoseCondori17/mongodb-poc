from beanie import Document
from pydantic import BaseModel

class Direccion(BaseModel):
    calle: str
    ciudad: str
    pais: str
    codigo_postal: str

class Customer(Document):
    nombre: str
    email: str
    telefono: str
    direccion: Direccion
    
    class Settings:
        name = "customers"