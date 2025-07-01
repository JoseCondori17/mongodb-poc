from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.product import router as product_router
from app.api.customer import router as customer_router
from app.api.order import router as order_router
from app.api.migrate import router as migrate_router
from app.database import connection
import uvicorn

async def lifespan(app: FastAPI):
    await connection()
    yield

app = FastAPI(
  title="API REST",
  version="v1",
  lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router, prefix="/product")
app.include_router(customer_router, prefix="/customer")
app.include_router(order_router, prefix="/order")
app.include_router(migrate_router, prefix="/migrate")

if __name__ == '__main__':
    uvicorn.run(app, port=8000)