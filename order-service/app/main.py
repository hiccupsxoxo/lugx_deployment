from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import List
import time

from app import models, schemas, crud
from app.database import SessionLocal, engine
from fastapi.responses import RedirectResponse

app = FastAPI()

# ✅ DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ DB auto-table creation on startup with retry
@app.on_event("startup")
def startup():
    retries = 10
    for i in range(retries):
        try:
            models.Base.metadata.create_all(bind=engine)
            print("✅ Orders table created.")
            break
        except OperationalError:
            print(f"⏳ Waiting for MySQL... ({i+1}/{retries})")
            time.sleep(3)
    else:
        raise RuntimeError("❌ Could not connect to MySQL after retries.")

# ✅ Redirect root to Swagger UI
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# ✅ Create order
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

# ✅ Get all orders
@app.get("/orders/", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

# ✅ Get order by ID
@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# ✅ Delete order
@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.delete_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
