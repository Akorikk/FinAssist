from sqlalchemy import text
from src.finassist.database.connection import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Database connected successfully!")
        print(result.scalar())

except Exception as e:
    print("Database connection failed!")
    print(e)