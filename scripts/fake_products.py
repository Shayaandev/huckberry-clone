
from database import SessionLocal
from models import Products

db = SessionLocal()

products = [
    Products(name="Trail Jacket", price=120.99, stock="100"),
    Products(name="Vintage Backpack", price=89.50 stock="100"),
    Products(name="Explorer Boots", price=150.00 stock="100")
    Produts(name)
]

db.add_all(products)
db.commit()
db.close()

print("Database seeded with fake data")


