from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import List
import time

from app import models, schemas, crud
from app.database import SessionLocal, engine

app = FastAPI()

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Startup event to create tables after DB is ready
@app.on_event("startup")
def startup():
    retries = 10
    for i in range(retries):
        try:
            models.Base.metadata.create_all(bind=engine)
            print("✅ Database tables created.")
            break
        except OperationalError:
            print(f"⏳ Waiting for DB... ({i+1}/{retries})")
            time.sleep(3)
    else:
        print("❌ Could not connect to DB after retries.")
        raise RuntimeError("Database connection failed after multiple retries.")

# ✅ Root route redirects to Swagger UI
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")

# ✅ POST /games/: Add a new game
@app.post("/games/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db=db, game=game)

# ✅ GET /games/: Retrieve all games
@app.get("/games/", response_model=List[schemas.Game])
def read_games(db: Session = Depends(get_db)):
    return crud.get_games(db)

# ✅ PUT /games/{game_id}: Update a game by ID
@app.put("/games/{game_id}", response_model=schemas.Game)
def update_game(game_id: int, game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_game = crud.update_game(db, game_id, game)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

# ✅ DELETE /games/{game_id}: Delete a game by ID
@app.delete("/games/{game_id}", response_model=schemas.Game)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    db_game = crud.delete_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game
