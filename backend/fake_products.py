from main import Base, engine, SessionLocal
from main import Products

Base.metadata.create_all(bind=engine)
db = SessionLocal()

products = [
    Products(name="Trail Jacket", price=120.99),
    Products(name="Vintage Backpack", price=89.50),
    Products(name="Explorer Boots", price=150.00)
]

db.add_all(products)
db.commit()
db.close()

print("Database seeded with fake data")

# =============for future reference========================

# from database import Base, engine, SessionLocal
# from models import Product

# Base.metadata.create_all(bind=engine)
# db = SessionLocal()

# products = [
#     Product(name="Trail Jacket", price=120.99, image="/images/jacket1.jpg", description="Waterproof outdoor jacket", category="Outerwear"),
#     Product(name="Vintage Backpack", price=89.50, image="/images/bag1.jpg", description="Military style canvas backpack", category="Accessories"),
#     Product(name="Explorer Boots", price=150.00, image="/images/boots1.jpg", description="Durable leather boots for hiking", category="Footwear")
# ]

# db.add_all(products)
# db.commit()
# db.close()

# print("Database seeded with fake products")
