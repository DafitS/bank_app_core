from abc import ABC, abstractmethod
from typing import Optional, List
from bank_app.domain.entities import Account

class AbstractAccountRepository(ABC):
    @abstractmethod
    def create(self, account: Account) -> Account:
        """
        Create a new account.

        Args:
            account (Account): The account entity to create.

        Returns:
            Account: The created account with assigned ID.
        """
        pass

    @abstractmethod
    def get_by_number(self, account_number: str) -> Optional[Account]:
        """
        Retrieve an account by its account number.

        Args:
            account_number (str): The account number.

        Returns:
            Optional[Account]: The account if found, else None.
        """
        pass

    
    @abstractmethod
    def update(self, account: Account) -> Account:
        """
        Update an existing account.

        Args:
            account (Account): The account entity with updated data.

        Returns:
            Account: The updated account entity.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Account]:
        """
        List all accounts in the system.

        Returns:
            List[Account]: All accounts.
        """
        pass

    @abstractmethod
    def disable(self, account: Account) -> None:
        pass