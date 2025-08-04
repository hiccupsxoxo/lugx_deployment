from pydantic import BaseModel

# Shared attributes for all operations (Create, Read, etc.)
class GameBase(BaseModel):
    title: str
    genre: str
    platform: str

# Schema for creating a game (no ID needed)
class GameCreate(GameBase):
    pass

# Schema for reading a game (includes ID from DB)
class Game(GameBase):
    id: int

    class Config:
        from_attributes = True  # Correct for Pydantic v2 (was orm_mode=True in v1)

