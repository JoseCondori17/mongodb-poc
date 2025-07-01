import asyncio
import random
from faker import Faker

from app.database import connection
from app.models.products import Product, ProductItem
from app.models.customers import Customer
from app.models.orders import Order

fake = Faker()

categories = {
    "Electronics": {
        "Laptops": ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple"],
        "Smartphones": ["Samsung", "Apple", "Xiaomi", "Motorola", "Huawei"],
        "Headphones": ["Sony", "JBL", "Bose", "Beats", "Sennheiser"],
        "Tablets": ["Samsung", "Apple", "Lenovo", "Huawei"]
    },
    "Home": {
        "Refrigerators": ["LG", "Samsung", "Whirlpool", "Bosch"],
        "Microwaves": ["Panasonic", "Samsung", "Daewoo", "Whirlpool"],
        "Vacuum Cleaners": ["Dyson", "Philips", "Electrolux", "LG"]
    },
    "Sports": {
        "Bicycles": ["Trek", "Giant", "Scott", "Specialized"],
        "Treadmills": ["NordicTrack", "ProForm", "Sole", "Horizon"],
        "Weights": ["Domyos", "Bowflex", "CAP", "Rogue"]
    },
    "Fashion": {
        "Sneakers": ["Nike", "Adidas", "Puma", "New Balance"],
        "Jackets": ["North Face", "Columbia", "Patagonia", "Uniqlo"],
        "Pants": ["Levi's", "Wrangler", "H&M", "Zara"]
    }
}

def generate_products():
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(list(categories[category].keys()))
    brand = random.choice(categories[category][subcategory])
    name = f"{subcategory[:-1] if subcategory.endswith('s') else subcategory} {brand}"
    price = round(random.uniform(50, 2500), 2)
    discount = random.choice([0, 5, 10, 15, 20])
    stock = random.randint(0, 100)
    dimensions = {
        "width": round(random.uniform(10.0, 50.0), 1),
        "height": round(random.uniform(2.0, 30.0), 1),
        "depth": round(random.uniform(1.0, 20.0), 1),
        "unit": "cm"
    }
    weight = {
        "value": round(random.uniform(0.2, 5.0), 2),
        "unit": "kg"
    }
    features = [fake.sentence(nb_words=6) for _ in range(random.randint(2, 5))]
    rating = round(random.uniform(1.0, 5.0), 1)
    description = fake.paragraph(nb_sentences=2)
    release_date = fake.date_between(start_date='-2y', end_date='today').isoformat()
    return {
        "name": name,
        "brand": brand,
        "price": price,
        "discount": discount,
        "category": category,
        "subcategory": subcategory,
        "stock": stock,
        "dimensions": dimensions,
        "weight": weight,
        "features": features,
        "rating": rating,
        "description": description,
        "release_date": release_date
    }

def generate_customers():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return {
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "country": fake.country(),
            "postal_code": fake.postcode()
        }
    }

async def insert_sample_data():
    """ Insert products and customers """
    await connection()

    # generate and insert products
    products = [Product(**generate_products()) for _ in range(100)]
    await Product.insert_many(products)
    print(f"Inserted {len(products)} products")

    # generate and insert customers
    customers = [Customer(**generate_customers()) for _ in range(100)]
    await Customer.insert_many(customers)
    print(f"Inserted {len(customers)} customer")

async def insert_orders_data():
    """ Insert orders """
    await connection()
    # get all data
    products = await Product.find().to_list(length=100)
    customers = await Customer.find().to_list(length=100)
    orders = []
    # generate 100 orders
    for _ in range(100):
        customer = random.choice(customers)
        selected_products = random.sample(products, k=random.randint(1, 3))
        order_products = [
            ProductItem(
                product_id=prod.id,
                name=prod.name,
                quantity=random.randint(1, 5),
                unit_price=prod.price
            ) for prod in selected_products]
        
        total = sum(p.quantity * p.unit_price for p in order_products)
        
        orders.append(Order(
            customer_id=customer.id,
            products=order_products,
            order_total=total,
            order_date=fake.date(),
            status=random.choice(["pending", "completed", "shipped"])
        ))
    print(f"Inserted {len(orders)} orders")
    
    await Order.insert_many(orders)

#asyncio.run(insert_sample_data())
#asyncio.run(insert_orders_data())