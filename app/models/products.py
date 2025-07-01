from beanie import Document
from pydantic import BaseModel
from datetime import date

class ProductItem(BaseModel):
    product_id: str
    nombre: str
    cantidad: int
    precio_unitario: float

class Dimension(BaseModel):
    ancho: float
    alto: float
    profundidad: float
    unidad: str
    
class Peso(BaseModel):
    valor: float
    unidad: str

class Product(Document):
    nombre: str
    marca: str
    precio: int
    descuento: int
    categoria: str
    subcategoria: str
    stock: int
    dimension: Dimension
    peso: Peso
    caracteristicas: list[str]
    calificacion: int
    descricion: str
    fecha_lanzamiento: date
    
    class Settings:
        name = "products"
        json_encoders = {
            date: lambda v: v.isoformat() # YYYY-mm-dd
        }