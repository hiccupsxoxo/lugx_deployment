from sqlalchemy.orm import Session
from app import models, schemas

# ✅ Create a new order
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        customer_name=order.customer_name,
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# ✅ Get all orders
def get_orders(db: Session):
    return db.query(models.Order).all()

# ✅ Get a specific order
def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# ✅ Delete an order
def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order
