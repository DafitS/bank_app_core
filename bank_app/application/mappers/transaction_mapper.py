from bank_app.domain.entities.transaction import Transaction
from bank_app.domain.dto.transaction_dto import TransactionDTORequest, TransactionDTOResponse

class TransactionMapper:

    @staticmethod
    def to_dto(transaction: Transaction) -> TransactionDTOResponse:
        return TransactionDTOResponse(
            transaction_id=str(transaction.transaction_id),
            account_number_from=transaction.account_number_from,
            account_number_to=transaction.account_number_to,
            amount=transaction.amount,
            created_at=transaction.created_at
        )

    @staticmethod
    def from_request(dto: TransactionDTORequest, transaction_id=None, created_at=None) -> Transaction:
        import uuid
        from decimal import Decimal
        return Transaction(
            transaction_id=transaction_id or uuid.uuid4(),
            account_number_from=dto.account_number_from,
            account_number_to=dto.account_number_to,
            amount=Decimal(dto.amount),
            created_at=created_at
        )