
from src.finassist.database.connection import engine, Base

# Import models so SQLAlchemy registers all table definitions.
from src.finassist.database import models


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)

        print("Database tables created successfully!")

        print("\nTables registered in SQLAlchemy:")

        for table_name in Base.metadata.tables:
            print(f"- {table_name}")

    except Exception as e:
        print("Failed to create database tables!")
        print(e)


if __name__ == "__main__":
    create_tables()
