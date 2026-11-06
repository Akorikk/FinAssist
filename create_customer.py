
from src.finassist.database.session import SessionLocal
from src.finassist.database.models import Customer


def create_customer():

    # Step 1: Create a database session
    db = SessionLocal()

    try:
        # Step 2: Create a Customer object
        customer = Customer(
            full_name="John Smith",
            email="john.smith@example.com",
            phone_number="+447700900123"
        )

        # Step 3: Add the customer to the session
        db.add(customer)

        # Step 4: Save the transaction in PostgreSQL
        db.commit()

        # Step 5: Refresh the object with database values
        db.refresh(customer)

        print("Customer created successfully!")
        print(f"Customer ID: {customer.customer_id}")
        print(f"Name: {customer.full_name}")
        print(f"Email: {customer.email}")

    except Exception as e:
        # Undo the transaction if something fails
        db.rollback()
        print(f"Error creating customer: {e}")

    finally:
        # Always close the database session
        db.close()


if __name__ == "__main__":
    create_customer()
