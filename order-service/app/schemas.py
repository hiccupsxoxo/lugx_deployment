from pydantic import BaseModel

# ✅ Shared attributes between create/read
class OrderBase(BaseModel):
    customer_name: str
    item_name: str
    quantity: int
    price: float
    status: str = "pending"

# ✅ Schema for creating orders (no ID)
class OrderCreate(OrderBase):
    pass

# ✅ Schema for reading orders (includes ID)
class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2 compatibility
