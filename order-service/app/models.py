from sqlalchemy import Column, Integer, String, Float
from app.database import Base

# ✅ Define the Order table
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
