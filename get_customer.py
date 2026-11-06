from sqlalchemy import select

from src.finassist.database.session import SessionLocal
from src.finassist.database.models import Customer


def get_customer():

    db = SessionLocal()

    try:
        # Build a SELECT query
        statement = select(Customer).where(
            Customer.email == "john.smith@example.com"
        )

        # Execute the query and retrieve one result
        customer = db.execute(statement).scalar_one_or_none()

        if customer:
            print("Customer found!")
            print(f"Customer ID: {customer.customer_id}")
            print(f"Name: {customer.full_name}")
            print(f"Email: {customer.email}")
            print(f"Account Status: {customer.account_status}")

        else:
            print("Customer not found!")

    except Exception as e:
        print(f"Error retrieving customer: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    get_customer()