from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from typing import Dict, Any
from app.models.products import Product

router = APIRouter()

@router.get("/")
async def products():
    try:
        products = await Product.find().to_list()
        return {
            "status": 200,
            "data": products,
            "message": "Get products successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/by-name/{product_name}")
async def search_by_name(product_name: str):
    try:
        products = await Product.find({"name": {"$regex": product_name, "$options": "i"}}).to_list()
        return {
            "status": 200,
            "data": products,
            "message": "Filtered by product name"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/by-id/{product_id}")
async def search_by_id(product_id: str):
    try:
        product = await Product.get(ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "status": 200,
            "data": product,
            "message": "Filtered by product id"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/remove/{product_id}")
async def delete_product(product_id: str):
    try:
        product = await Product.get(ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        await product.delete()

        return {
            "status": 200,
            "message": "Product deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/filter")
async def filter_products(filter: Dict[str, Any] = Body(...)):
    try:
        products = await Product.find(filter).to_list()
        return {
            "status": 200,
            "data": products,
            "message": "Filtered products successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/new")
async def new_product(product: Product):
    try:
        await Product.insert(product)
        return {
            "status": 200,
            "message": "Created product successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# aggregations
@router.get("/counts")
async def count_products():
    try:
        count = await Product.count()
        return {
            "status": 200,
            "data": count,
            "message": "Get count products successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/stock-by-category")
async def stock_by_category():
    try:
        pipeline = [
            { "$sort": { "category": 1, "stock": -1 } },
            { "$group": {
                "_id": "$category",
                "product": { "$first": "$name" },
                "stock": { "$first": "$stock" }
            }},
            { "$limit": 5 }
        ]
        result = await Product.aggregate(pipeline).to_list()

        if result:
            return {
                "status": 200,
                "data": result,
                "message": "Get stock by category successfully"
            }
        else:
            return {
                "status": 204,
                "message": "No data available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/average-price")
async def average_price():
    try:
        pipeline = [
            { "$group": { "_id": None, "average_price": { "$avg": "$price" } } }
        ]
        result = await Product.aggregate(pipeline).to_list()

        if result:
            return {
                "status": 200,
                "average_price": result,
                "message": "Average price calculated successfully"
            }
        else:
            return {
                "status": 204,
                "message": "No data available"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
