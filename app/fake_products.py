
from database import SessionLocal
from models import Products

db = SessionLocal()

products = [
    Products(name="Classic White T-Shirt", price=19.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Graphic Tee", price=24.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Black Polo Shirt", price=29.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Casual Button-up Shirt", price=34.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Slim Fit Dress Shirt", price=39.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Grey Hoodie", price=49.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Crewneck Sweatshirt", price=44.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Button Cardigan", price=54.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="Crop Top", price=22.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Cotton Tank Top", price=18.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Skinny Jeans", price=59.99, stock=35, image_url="/static/images/placeholder.png"),
    Products(name="Straight Leg Jeans", price=59.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Chino Pants", price=49.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Cargo Shorts", price=34.99, stock=45, image_url="/static/images/placeholder.png"),
    Products(name="Casual Shorts", price=29.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Joggers", price=39.99, stock=35, image_url="/static/images/placeholder.png"),
    Products(name="Leggings", price=24.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Mini Skirt", price=29.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Midi Skirt", price=34.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Maxi Skirt", price=39.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="Bomber Jacket", price=69.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Denim Jacket", price=64.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Leather Jacket", price=129.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="Winter Parka", price=149.99, stock=10, image_url="/static/images/placeholder.png"),
    Products(name="Windbreaker", price=59.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Trench Coat", price=119.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="Peacoat", price=109.99, stock=12, image_url="/static/images/placeholder.png"),
    Products(name="Puffer Jacket", price=139.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="White Sneakers", price=69.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Running Shoes", price=89.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Leather Boots", price=129.99, stock=15, image_url="/static/images/placeholder.png"),
    Products(name="Casual Loafers", price=79.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Summer Sandals", price=34.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Wool Slippers", price=29.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Baseball Cap", price=19.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Beanie", price=14.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Bucket Hat", price=24.99, stock=35, image_url="/static/images/placeholder.png"),
    Products(name="Scarf", price=29.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Gloves", price=19.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Leather Belt", price=24.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="Sunglasses", price=49.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Wrist Watch", price=149.99, stock=10, image_url="/static/images/placeholder.png"),
    Products(name="Cotton Socks", price=9.99, stock=100, image_url="/static/images/placeholder.png"),
    Products(name="Wool Socks", price=12.99, stock=80, image_url="/static/images/placeholder.png"),
    Products(name="Swim Trunks", price=29.99, stock=30, image_url="/static/images/placeholder.png"),
    Products(name="One-piece Swimsuit", price=39.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Pajama Set", price=49.99, stock=25, image_url="/static/images/placeholder.png"),
    Products(name="Yoga Pants", price=34.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Sports Bra", price=24.99, stock=35, image_url="/static/images/placeholder.png"),
    Products(name="Gym Shorts", price=29.99, stock=40, image_url="/static/images/placeholder.png"),
    Products(name="Raincoat", price=59.99, stock=20, image_url="/static/images/placeholder.png"),
    Products(name="Winter Mittens", price=14.99, stock=50, image_url="/static/images/placeholder.png"),
    Products(name="Formal Suit", price=199.99, stock=10, image_url="/static/images/placeholder.png"),
    Products(name="Tie", price=19.99, stock=40, image_url="/static/images/placeholder.png")
]

db.query(Products).delete()
db.add_all(products)
db.commit()
db.close()

print("Database seeded with fake data")


