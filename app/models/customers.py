from beanie import Document
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Customer(Document):
    name: str
    email: str
    phone: str
    address: Address
    
    class Settings:
        name = "customers"