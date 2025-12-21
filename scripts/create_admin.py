# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User
from database import SessionLocal
from auth import hash_password

db = SessionLocal()

admin = User(
    username="admin",
    hashed_password=hash_password("admin123"),
    is_admin=True
)

db.add(admin)
db.commit()
db.close()