import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Load DB connection from environment (docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@orderdb:3306/orders")

# ✅ SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()
