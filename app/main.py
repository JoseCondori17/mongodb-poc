from fastapi import FastAPI
from app.api.product import router as product_router
from app.api.customer import router as customer_router
from app.api.order import route as order_router
import uvicorn

app = FastAPI(
  title="API REST",
  version="v1"
)

app.include_router(product_router, prefix="/product")
app.include_router(customer_router, prefix="/customer")
app.include_router(order_router, prefix="/order")

if __name__ == '__main__':
    uvicorn.run(app, port=8000)