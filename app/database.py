from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Формат URL: postgresql://user:password@localhost:5432/db_name
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/pharmacy_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
