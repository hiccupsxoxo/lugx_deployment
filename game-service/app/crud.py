from sqlalchemy.orm import Session
from . import models, schemas

# Create a new game
def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(
        title=game.title,
        genre=game.genre,
        platform=game.platform
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

# Read all games
def get_games(db: Session):
    return db.query(models.Game).all()

# Update a game by ID
def update_game(db: Session, game_id: int, updated_game: schemas.GameCreate):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        return None

    db_game.title = updated_game.title
    db_game.genre = updated_game.genre
    db_game.platform = updated_game.platform

    db.commit()
    db.refresh(db_game)
    return db_game

# Delete a game by ID
def delete_game(db: Session, game_id: int):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        return None
    db.delete(db_game)
    db.commit()
    return db_game
