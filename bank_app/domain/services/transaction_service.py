from decimal import Decimal
import uuid
from bank_app.application.mappers.transaction_mapper import TransactionMapper
from bank_app.domain.dto.transaction_dto import TransactionDTORequest, TransactionDTOResponse
from bank_app.infrastructure.orm.operation_history import OperationHistory
from bank_app.domain.entities.transaction import Transaction
from bank_app.domain.exceptions.custom_exceptions import NotFoundError, AmountTooSmallError

class TransactionService:
    def __init__(self, account_repo, transaction_repo, operation_repo):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.operation_repo = operation_repo

    def transfer(self, transfer_request: TransactionDTORequest) -> TransactionDTOResponse:
        account_from_number = transfer_request.account_number_from
        account_to_number = transfer_request.account_number_to
        amount = Decimal(transfer_request.amount)

        if amount <= 0:
            raise AmountTooSmallError("Amount must be greater than 0")

        account_from = self.account_repo.get_by_number(account_from_number)
        account_to = self.account_repo.get_by_number(account_to_number)

        if not account_from or not account_to:
            raise NotFoundError("Account not found")
        if account_from_number == account_to_number:
            raise ValueError("Cannot transfer to the same account")
        if account_from.amount < amount:
            raise AmountTooSmallError("Insufficient funds")
        if not account_from.active or not account_to.active:
            raise ValueError("One of the accounts is inactive")

       
        account_from.amount -= amount
        account_to.amount += amount

        
        self.account_repo.update(account_from)
        self.account_repo.update(account_to)

        
        transaction = TransactionMapper.from_request(transfer_request)

        transaction = self.transaction_repo.create(
            transaction,
            account_from_id=account_from.account_id,
            account_to_id=account_to.account_id
        )

        operation_out = OperationHistory(
            operation_id=uuid.uuid4(),
            account_id=account_from.account_id,
            operation_type="transfer_out",
            amount=amount,
            account_from_id=account_from.account_id,
            account_to_id=account_to.account_id
        )
        self.operation_repo.create(operation_out)

        operation_in = OperationHistory(
            operation_id=uuid.uuid4(),
            account_id=account_to.account_id,
            operation_type="transfer_in",
            amount=amount,
            account_from_id=account_from.account_id,
            account_to_id=account_to.account_id
        )
        self.operation_repo.create(operation_in)

        return TransactionMapper.to_dto(transaction)