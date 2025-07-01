from motor.motor_asyncio import AsyncIOMotorClient
from models.products import Product
from models.customers import Customer
from models.orders import Order

from beanie import init_beanie

MONGO_URI = "mongodb://localhost:27017"

async def connection():
    client = AsyncIOMotorClient(MONGO_URI)

    await init_beanie(database=client.ecommerce, document_models=[
        Product,
        Customer,
        Order
    ])

