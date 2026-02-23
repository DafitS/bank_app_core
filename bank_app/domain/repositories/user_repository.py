from abc import ABC, abstractmethod
from typing import Optional, List
from bank_app.domain.entities import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        """
        Create a new user.

        Args:
            user (User): The user entity to create.

        Returns:
            User: The created user with assigned ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The user if found, else None.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: The user if found, else None.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        """
        List all users.

        Returns:
            List[User]: List of all users.
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Update an existing user.

        Args:
            user (User): The user entity with updated data.

        Returns:
            User: The updated user entity.
        """
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """
        Delete a user.

        Args:
            user (User): The user entity to delete.

        Returns:
            None
        """
        pass
