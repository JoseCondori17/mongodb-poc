from faker import Faker
from database import connection
import random

fake = Faker()

categorias = {
    "Electrónica": {
        "Laptops": ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple"],
        "Smartphones": ["Samsung", "Apple", "Xiaomi", "Motorola", "Huawei"],
        "Auriculares": ["Sony", "JBL", "Bose", "Beats", "Sennheiser"],
        "Tablets": ["Samsung", "Apple", "Lenovo", "Huawei"]
    },
    "Hogar": {
        "Refrigeradoras": ["LG", "Samsung", "Whirlpool", "Bosch"],
        "Microondas": ["Panasonic", "Samsung", "Daewoo", "Whirlpool"],
        "Aspiradoras": ["Dyson", "Philips", "Electrolux", "LG"]
    },
    "Deportes": {
        "Bicicletas": ["Trek", "Giant", "Scott", "Specialized"],
        "Trotadoras": ["NordicTrack", "ProForm", "Sole", "Horizon"],
        "Pesas": ["Domyos", "Bowflex", "CAP", "Rogue"]
    },
    "Moda": {
        "Zapatillas": ["Nike", "Adidas", "Puma", "New Balance"],
        "Casacas": ["North Face", "Columbia", "Patagonia", "Uniqlo"],
        "Pantalones": ["Levi's", "Wrangler", "H&M", "Zara"]
    }
}

def generate_products():
    categoria = random.choice(list(categorias.keys()))
    subcategoria = random.choice(list(categorias[categoria].keys()))
    marca = random.choice(categorias[categoria][subcategoria])
    nombre = f"{subcategoria[:-1] if subcategoria.endswith('s') else subcategoria} {marca}"
    precio = round(random.uniform(50, 2500), 2)
    descuento = random.choice([0, 5, 10, 15, 20])
    stock = random.randint(0, 100)
    dimensiones = {
        "ancho": round(random.uniform(10.0, 50.0), 1),
        "alto": round(random.uniform(2.0, 30.0), 1),
        "profundidad": round(random.uniform(1.0, 20.0), 1),
        "unidad": "cm"
    }
    peso = {
        "valor": round(random.uniform(0.2, 5.0), 2),
        "unidad": "kg"
    }
    caracteristicas = [fake.sentence(nb_words=6) for _ in range(random.randint(2, 5))]
    calificacion = round(random.uniform(1.0, 5.0), 1)
    descripcion = fake.paragraph(nb_sentences=2)
    fecha_lanzamiento = fake.date_between(start_date='-2y', end_date='today').isoformat()
    return {
        "nombre": nombre,
        "marca": marca,
        "precio": precio,
        "descuento": descuento,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "stock": stock,
        "dimensiones": dimensiones,
        "peso": peso,
        "caracteristicas": caracteristicas,
        "calificacion": calificacion,
        "descripcion": descripcion,
        "fecha_lanzamiento": fecha_lanzamiento
    }

def generate_customers(): ...

productos = [generate_products() for _ in range(100)]