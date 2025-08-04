import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# ✅ Read from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mysql:3306/gamedb")

engine = create_engine(
    DATABASE_URL,
    connect_args={"charset": "utf8mb4"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
