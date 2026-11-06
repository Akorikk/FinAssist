
import calendar

from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select

from src.finassist.database.session import SessionLocal

from src.finassist.database.models import (
    Customer,
    LoanAccount,
    Repayment,
    SupportTicket,
    HardshipCase,
    AuditLog,
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

def add_months(original_date: date, months: int) -> date:
    """Add months to a date while handling different month lengths."""

    month_index = original_date.month - 1 + months

    year = original_date.year + month_index // 12
    month = month_index % 12 + 1

    day = min(
        original_date.day,
        calendar.monthrange(year, month)[1]
    )

    return date(year, month, day)


CUSTOMERS = [
    ("John Smith", "john.smith@example.com"),
    ("Emma Wilson", "emma.wilson@example.com"),
    ("Oliver Brown", "oliver.brown@example.com"),
    ("Sophia Taylor", "sophia.taylor@example.com"),
    ("James Anderson", "james.anderson@example.com"),
    ("Isabella Thomas", "isabella.thomas@example.com"),
    ("William Jackson", "william.jackson@example.com"),
    ("Mia White", "mia.white@example.com"),
    ("Lucas Harris", "lucas.harris@example.com"),
    ("Amelia Martin", "amelia.martin@example.com"),
]

LOAN_AMOUNTS = [
    Decimal("5000.00"),
    Decimal("7500.00"),
    Decimal("10000.00"),
    Decimal("3500.00"),
    Decimal("12000.00"),
    Decimal("6000.00"),
    Decimal("8500.00"),
    Decimal("15000.00"),
    Decimal("4000.00"),
    Decimal("9000.00"),
]

SUPPORT_TICKET_DATA = {
    0: (
        "loan_repayment",
        "Customer needs clarification about the next repayment.",
        "normal",
    ),
    1: (
        "account_support",
        "Customer reports difficulty accessing account information.",
        "normal",
    ),
    3: (
        "payment_issue",
        "Customer says a repayment has not been reflected in the account.",
        "high",
    ),
    5: (
        "loan_repayment",
        "Customer requests information about their repayment schedule.",
        "normal",
    ),
    7: (
        "financial_hardship",
        "Customer reports a reduction in monthly income.",
        "high",
    ),
    9: (
        "account_support",
        "Customer needs assistance understanding loan account details.",
        "normal",
    ),
}

HARDSHIP_DATA = {
    2: (
        "job_loss",
        "Customer reports losing employment and struggling to maintain repayments.",
        "Information about available financial difficulty support.",
    ),
    4: (
        "reduced_income",
        "Customer reports a significant reduction in monthly income.",
        "Help understanding available repayment support options.",
    ),
    6: (
        "unexpected_expenses",
        "Customer reports unexpected household expenses affecting repayments.",
        "Request for a review by a financial support specialist.",
    ),
    8: (
        "medical_expenses",
        "Customer reports increased expenses and difficulty meeting repayments.",
        "Information about the financial hardship review process.",
    ),
}


# --------------------------------------------------
# MAIN DATA GENERATOR
# --------------------------------------------------

def seed_synthetic_data():

    db = SessionLocal()

    customer_count = 0
    loan_count = 0
    repayment_count = 0
    ticket_count = 0
    hardship_count = 0
    audit_count = 0
    skipped_count = 0

    today = date.today()

    try:

        for index, (full_name, email) in enumerate(CUSTOMERS):

            # Check whether this synthetic customer already exists.
            existing_customer = db.scalar(
                select(Customer).where(Customer.email == email)
            )

            if existing_customer:
                print(f"Skipping existing customer: {email}")
                skipped_count += 1
                continue

            # ------------------------------------------
            # 1. CREATE CUSTOMER
            # ------------------------------------------

            customer = Customer(
                full_name=full_name,
                email=email,
                phone_number=f"+447700900{100 + index}",
                account_status="active",
            )

            # ------------------------------------------
            # 2. CREATE LOAN ACCOUNT
            # ------------------------------------------

            principal = LOAN_AMOUNTS[index]

            loan_start_date = add_months(today, -8)

            loan = LoanAccount(
                customer=customer,
                principal_amount=principal,
                annual_interest_rate=Decimal("8.5000"),
                term_months=36,
                start_date=loan_start_date,
                end_date=add_months(loan_start_date, 36),
                loan_status="active",
                currency="GBP",
            )

            # ------------------------------------------
            # 3. CREATE 12 REPAYMENT RECORDS
            # ------------------------------------------

            monthly_amount = (
                principal / Decimal("36")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            for month_number in range(12):

                due_date = add_months(
                    today,
                    month_number - 7
                )

                if month_number < 6:
                    payment_status = "paid"
                    amount_paid = monthly_amount
                    paid_at = datetime.now(timezone.utc)

                elif due_date < today:
                    payment_status = "overdue"
                    amount_paid = Decimal("0.00")
                    paid_at = None

                else:
                    payment_status = "pending"
                    amount_paid = Decimal("0.00")
                    paid_at = None

                repayment = Repayment(
                    loan=loan,
                    due_date=due_date,
                    amount_due=monthly_amount,
                    amount_paid=amount_paid,
                    paid_at=paid_at,
                    payment_status=payment_status,
                )

                db.add(repayment)
                repayment_count += 1

            # ------------------------------------------
            # 4. CREATE SUPPORT TICKET WHEN APPLICABLE
            # ------------------------------------------

            if index in SUPPORT_TICKET_DATA:

                category, description, priority = (
                    SUPPORT_TICKET_DATA[index]
                )

                ticket = SupportTicket(
                    customer=customer,
                    category=category,
                    description=description,
                    priority=priority,
                    ticket_status="open",
                )

                db.add(ticket)
                ticket_count += 1

            # ------------------------------------------
            # 5. CREATE HARDSHIP CASE WHEN APPLICABLE
            # ------------------------------------------

            if index in HARDSHIP_DATA:

                reason, description, requested_support = (
                    HARDSHIP_DATA[index]
                )

                hardship_case = HardshipCase(
                    customer=customer,
                    loan=loan,
                    reason_category=reason,
                    customer_description=description,
                    requested_support=requested_support,
                    case_status="pending_review",
                    assigned_to=None,
                )

                db.add(hardship_case)
                hardship_count += 1

            # Add customer and related records to session.
            db.add(customer)

            # Flush to generate the customer's UUID.
            db.flush()

            # ------------------------------------------
            # 6. CREATE AUDIT LOG
            # ------------------------------------------

            audit_log = AuditLog(
                actor_type="system",
                actor_id=None,
                action="seed_synthetic_customer",
                resource_type="customer",
                resource_id=customer.customer_id,
                outcome="success",
                details={
                    "source": "synthetic_data_generator",
                    "environment": "development",
                },
            )

            db.add(audit_log)
            audit_count += 1

            customer_count += 1
            loan_count += 1

            print(f"Prepared customer: {full_name}")

        # ------------------------------------------
        # COMMIT ALL DATABASE CHANGES
        # ------------------------------------------

        db.commit()

        print("\n====================================")
        print("SYNTHETIC DATA GENERATION COMPLETED")
        print("====================================")

        print(f"Customers created:       {customer_count}")
        print(f"Loans created:           {loan_count}")
        print(f"Repayments created:      {repayment_count}")
        print(f"Support tickets created: {ticket_count}")
        print(f"Hardship cases created:  {hardship_count}")
        print(f"Audit logs created:      {audit_count}")
        print(f"Customers skipped:       {skipped_count}")

        print("====================================")

    except Exception as error:

        db.rollback()

        print("\nSynthetic data generation failed!")
        print(f"Error: {error}")

    finally:

        db.close()


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    seed_synthetic_data()
