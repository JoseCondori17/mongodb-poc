from motor.motor_asyncio import AsyncIOMotorClient
from app.models.products import Product, ProductCloud
from app.models.customers import Customer
from app.models.orders import Order
from app.models.categories import Category

from beanie import init_beanie

MONGO_URI = "mongodb://localhost:27017"

async def connection():
    client = AsyncIOMotorClient(MONGO_URI)

    await init_beanie(database=client.ecommerce, document_models=[
        Product,
        ProductCloud,
        Customer,
        Order,
        Category,
    ])

