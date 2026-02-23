from decimal import Decimal
import uuid
from bank_app.domain.entities.transaction import Transaction
from bank_app.domain.exceptions.custom_exceptions import NotFoundError, AmountTooSmallError

class TransactionService:
    def __init__(self, account_repo, transaction_repo):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def transfer(self, account_from_number: str, account_to_number: str, amount: Decimal):
        amount = Decimal(amount)
        account_from_number = str(account_from_number)
        account_to_number = str(account_to_number)

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

        
        transaction = Transaction(
            transaction_id=uuid.uuid4(),
            account_number_from=account_from.account_number,
            account_number_to=account_to.account_number,
            amount=amount
        )

        transaction = self.transaction_repo.create(
            transaction,
            account_from_id=account_from.account_id,
            account_to_id=account_to.account_id
        )

        return transaction