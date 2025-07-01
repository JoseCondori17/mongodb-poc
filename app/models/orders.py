from beanie import Document, Link
from datetime import date
from app.models.products import ProductItem
from app.models.customers import Customer

class Order(Document):
    customer_id: Link[Customer]
    products: list[ProductItem]
    order_total: float
    order_date: date
    status: str

    class Settings:
        name = "orders"
        json_encoders = {
            date: lambda v: v.isoformat() # YYYY-mm-dd
        }