from beanie import Document, Link
from pydantic import BaseModel
from datetime import date

class Dimension(BaseModel):
    width: float
    height: float
    depth: float
    unit: str
    
class Weight(BaseModel):
    value: float
    unit: str

class Product(Document):
    name: str
    brand: str
    price: float
    discount: int
    category: str
    subcategory: str
    stock: int
    dimensions: Dimension
    weight: Weight
    features: list[str]
    rating: float
    description: str
    release_date: date
    
    class Settings:
        name = "products"
        json_encoders = {
            date: lambda v: v.isoformat() # YYYY-mm-dd
        }

class ProductItem(BaseModel):
    product_id: Link[Product]
    name: str
    quantity: int
    unit_price: float


# other prodcut
class ProductCloud(Document):
    model_config = {
        "extra": "allow"
    }

    class Settings:
        name = "products_cloud"