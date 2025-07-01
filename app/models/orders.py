from beanie import Document
from pydantic import BaseModel
from datetime import date
from models.products import ProductItem

class Order(Document):
    id_cliente: str
    productos: list[ProductItem]
    total_pedido: int
    fecha_pedido: date
    estado: str