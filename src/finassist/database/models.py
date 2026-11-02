
import uuid

from datetime import datetime, date, timezone
from decimal import Decimal

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Integer,
    Date,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID, JSONB

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.finassist.database.connection import Base


# ============================================================
# 1. CUSTOMER MODEL
# ============================================================

class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    account_status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # One customer can have multiple loans.
    loans: Mapped[list["LoanAccount"]] = relationship(
        back_populates="customer"
    )

    # One customer can have multiple support tickets.
    support_tickets: Mapped[list["SupportTicket"]] = relationship(
        back_populates="customer"
    )

    # One customer can have multiple hardship cases.
    hardship_cases: Mapped[list["HardshipCase"]] = relationship(
        back_populates="customer"
    )


# ============================================================
# 2. LOAN ACCOUNT MODEL
# ============================================================

class LoanAccount(Base):
    __tablename__ = "loan_accounts"

    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
        index=True
    )

    # Decimal is used for accurate financial values.
    principal_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    annual_interest_rate: Mapped[Decimal] = mapped_column(
        Numeric(7, 4),
        nullable=False
    )

    term_months: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    loan_status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="GBP",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with Customer.
    customer: Mapped["Customer"] = relationship(
        back_populates="loans"
    )

    # One loan can have multiple repayments.
    repayments: Mapped[list["Repayment"]] = relationship(
        back_populates="loan"
    )


# ============================================================
# 3. REPAYMENT MODEL
# ============================================================

class Repayment(Base):
    __tablename__ = "repayments"

    repayment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_accounts.loan_id"),
        nullable=False,
        index=True
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    amount_due: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    amount_paid: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with LoanAccount.
    loan: Mapped["LoanAccount"] = relationship(
        back_populates="repayments"
    )


# ============================================================
# 4. SUPPORT TICKET MODEL
# ============================================================

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
        index=True
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="normal",
        nullable=False
    )

    ticket_status: Mapped[str] = mapped_column(
        String(20),
        default="open",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with Customer.
    customer: Mapped["Customer"] = relationship(
        back_populates="support_tickets"
    )


# ============================================================
# 5. HARDSHIP CASE MODEL
# ============================================================

class HardshipCase(Base):
    __tablename__ = "hardship_cases"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
        index=True
    )

    loan_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_accounts.loan_id"),
        nullable=True
    )

    reason_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    customer_description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    requested_support: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    case_status: Mapped[str] = mapped_column(
        String(30),
        default="pending_review",
        nullable=False
    )

    assigned_to: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with Customer.
    customer: Mapped["Customer"] = relationship(
        back_populates="hardship_cases"
    )

    # A hardship case may be linked to a loan.
    loan: Mapped["LoanAccount | None"] = relationship()


# ============================================================
# 6. AUDIT LOG MODEL
# ============================================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    actor_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    resource_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    outcome: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    details: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
