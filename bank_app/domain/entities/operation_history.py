import uuid
from datetime import datetime
from decimal import Decimal


class OperationHistory:
    def __init__(
        self,
        id: uuid.UUID,
        account_id: int,
        operation_type: str,
        amount: Decimal,
        account_from_id: str | None = None,
        account_to_id: str | None = None,
        created_at: datetime | None = None
    ):
        self.id = id
        self.account_id = account_id
        self.operation_type = operation_type
        self.amount = amount
        self.account_from_id = account_from_id
        self.account_to_id = account_to_id
        self.created_at = created_at

    def __repr__(self):
        return (
            f"OperationHistory(id={self.id}, "
            f"account_id={self.account_id}, "
            f"operation_type={self.operation_type}, "
            f"amount={self.amount}, "
            f"account_from_id={self.account_from_id}, "
            f"account_to_id={self.account_to_id}, "
            f"created_at={self.created_at})"
        )
