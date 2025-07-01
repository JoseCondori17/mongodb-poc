from fastapi import APIRouter, HTTPException
import requests

from app.models.categories import Category
from app.models.products import Product, ProductCloud

router = APIRouter()

@router.post("/migrate-categories")
async def migrate_categories():
    response = requests.get("https://dummyjson.com/products/categories")
    if response.status_code == 200:
        categories_json = response.json()
        categories = [Category(**category) for category in categories_json]
        try: 
            await Category.insert_many(categories)
            return {
                "status": 200, "message": "Migration correctly"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error inserting categories: {str(e)}")

@router.post("/migrate-products")
async def migrate_products():
    products = []
    response = requests.get("https://dummyjson.com/products/categories")
    if response.status_code == 200:
        categories_json = response.json()
        urls = [category["url"] for category in categories_json]
        for url in urls:
            product_response = requests.get(url)
            product_json = product_response.json()
            products_data = product_json["products"]
            for p in products_data:
                clean_product = {k: v for k, v in p.items() if k != "id"}
                products.append(ProductCloud(**clean_product))
    try:
        if products:
            await ProductCloud.insert_many(products)
            return {
                "status": 200, "message": "Migration correctly"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting products: {str(e)}")