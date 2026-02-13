import os
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta

from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session, sessionmaker

import exceptions as ex
from orm import Accounts, Transactions, Users
from utils import generate_unique_account_number, pwd_context

SECRET_KEY: str | None = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM: str = "HS256"


class BankAppHandler:
    """Service layer responsible for banking operations.

    Handles database sessions, users, accounts, transactions
    and authentication-related logic.
    """

    def __init__(self) -> None:
        """Initialize database engine and session factory.

        Raises:
            RuntimeError: If database URL is not provided.
        """
        database_url: str | None = os.getenv("URL")
        if not database_url:
            raise RuntimeError("Database URL is not set")

        self.engine = create_engine(database_url)
        self.session = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provide a transactional SQLAlchemy session.

        Commits the transaction on success and rolls back
        in case of any exception.

        Yields:
            Session: Active SQLAlchemy session.

        Raises:
            DuplictedError: If integrity constraint is violated.
            NotFoundError: If queried record does not exist.
        """
        session: Session = self.session()
        try:
            yield session
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise ex.DuplictedError("Record already exists!") from exc
        except NoResultFound as exc:
            session.rollback()
            raise ex.NotFoundError("Record not found!") from exc
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_account(self, user_id: int) -> dict[str, int | float | str]:
        """Create a new bank account for an existing user.

        Args:
            user_id: ID of the user.

        Returns:
            Dictionary containing created account data.

        Raises:
            NotFoundError: If user does not exist.
        """
        with self.get_session() as session:
            user = (
                session.query(Users)
                .filter_by(user_id=user_id)
                .one_or_none()
            )
            if user is None:
                raise ex.NotFoundError("User does not exist")

            account = Accounts(
                account_number=generate_unique_account_number(),
                user_id=user_id,
            )
            session.add(account)
            session.flush()

            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "user_id": user_id,
                "amount": account.amount,
            }

    def get_accounts(self) -> list[dict[str, int | float | str]]:
        """Return all bank accounts.

        Returns:
            List of accounts represented as dictionaries.
        """
        with self.get_session() as session:
            accounts = session.query(Accounts).all()
            return [
                {
                    "account_id": acc.account_id,
                    "account_number": acc.account_number,
                    "amount": acc.amount,
                    "user_id": acc.user_id,
                }
                for acc in accounts
            ]

    def delete_account(self, number: str) -> None:
        """Delete account by account number.

        Args:
            number: Account number.

        Raises:
            NotFoundError: If account does not exist.
        """
        with self.get_session() as session:
            account = (
                session.query(Accounts)
                .filter_by(account_number=number)
                .one_or_none()
            )
            if account is None:
                raise ex.NotFoundError(f"Account {number} not found")

            session.delete(account)

    def create_user(self, email: str, password: str) -> dict[str, int | str]:
        """Create a new user and assign a default account.

        Args:
            email: User email address.
            password: Plain-text password.

        Returns:
            Dictionary with user and account identifiers.
        """
        hashed_password = pwd_context.hash(password)

        with self.get_session() as session:
            user = Users(email=email, password=hashed_password)
            session.add(user)
            session.flush()

            account = Accounts(
                account_number=generate_unique_account_number(),
                user_id=user.user_id,
            )
            session.add(account)
            session.flush()

            return {
                "id": user.user_id,
                "email": user.email,
                "account_id": account.account_id,
            }

    def get_users(self) -> list[dict[str, int | str | None]]:
        """Return all users.

        Returns:
            List of users with basic information.
        """
        with self.get_session() as session:
            users = session.query(Users).all()
            return [
                {
                    "id": user.user_id,
                    "email": user.email,
                    "account_id": (
                        user.accounts[0].account_id
                        if user.accounts
                        else None
                    ),
                }
                for user in users
            ]

    def delete_user(self, user_id: int) -> None:
        """Delete user by ID.

        Args:
            user_id: User identifier.

        Raises:
            NotFoundError: If user does not exist.
        """
        with self.get_session() as session:
            user = (
                session.query(Users)
                .filter_by(user_id=user_id)
                .one_or_none()
            )
            if user is None:
                raise ex.NotFoundError(f"User {user_id} not found")

            session.delete(user)

    def update_account(
        self,
        number: str,
        new_amount: float,
    ) -> dict[str, int | float | str]:
        """Update account balance.

        Args:
            number: Account number.
            new_amount: New account balance.

        Returns:
            Updated account data.

        Raises:
            NotFoundError: If account does not exist.
        """
        with self.get_session() as session:
            account = (
                session.query(Accounts)
                .filter_by(account_number=number)
                .one_or_none()
            )
            if account is None:
                raise ex.NotFoundError(f"Account {number} not found")

            account.amount = new_amount
            session.flush()

            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "amount": account.amount,
                "user_id": account.user_id,
            }

    def update_user(
        self,
        user_id: int,
        new_email: str,
    ) -> dict[str, int | str]:
        """Update user's email address.

        Args:
            user_id: User identifier.
            new_email: New email address.

        Returns:
            Updated user data.

        Raises:
            NotFoundError: If user does not exist.
            DuplictedError: If email is already in use.
        """
        with self.get_session() as session:
            user = (
                session.query(Users)
                .filter_by(user_id=user_id)
                .one_or_none()
            )
            if user is None:
                raise ex.NotFoundError(f"User {user_id} not found")

            existing_email = (
                session.query(Users)
                .filter_by(email=new_email)
                .one_or_none()
            )
            if existing_email and existing_email.user_id != user_id:
                raise ex.DuplictedError("Email already in use!")

            user.email = new_email
            session.flush()

            return {
                "id": user.user_id,
                "email": user.email,
            }

    def create_transaction(
        self,
        account_from_id: int,
        account_to_id: int,
        amount: float,
    ) -> dict[str, int | float]:
        """Transfer money between two accounts.

        Args:
            account_from_id: Sender account ID.
            account_to_id: Receiver account ID.
            amount: Transfer amount.

        Returns:
            Transaction details.

        Raises:
            NotFoundError: If any account does not exist.
            AmountTooSmallError: If sender has insufficient funds.
        """
        with self.get_session() as session:
            acc_from = (
                session.query(Accounts)
                .filter_by(account_id=account_from_id)
                .one_or_none()
            )
            acc_to = (
                session.query(Accounts)
                .filter_by(account_id=account_to_id)
                .one_or_none()
            )

            if not acc_from:
                raise ex.NotFoundError(
                    f"Account {account_from_id} does not exist!"
                )
            if not acc_to:
                raise ex.NotFoundError(
                    f"Account {account_to_id} does not exist!"
                )
            if acc_from.amount < amount:
                raise ex.AmountTooSmallError(
                    "Too little money in account!"
                )

            acc_from.amount -= amount
            acc_to.amount += amount

            transaction = Transactions(
                account_id_from=account_from_id,
                account_id_to=account_to_id,
                amount=amount,
            )
            session.add(transaction)
            session.flush()

            return {
                "transaction_id": transaction.transaction_id,
                "account_from_id": account_from_id,
                "account_to_id": account_to_id,
                "amount": amount,
            }

    def authenticate(self, email: str, password: str) -> Users:
        """Authenticate user credentials.

        Args:
            email: User email.
            password: Plain-text password.

        Returns:
            Authenticated user ORM object.

        Raises:
            AuthenticationException: If credentials are invalid.
        """
        with self.get_session() as session:
            user = (
                session.query(Users)
                .filter_by(email=email)
                .one_or_none()
            )
            if user is None:
                raise ex.AuthenticationException(
                    "Wrong email or password!"
                )

            if not pwd_context.verify(password, user.password):
                raise ex.AuthenticationException(
                    "Wrong email or password!"
                )

            return user

    @staticmethod
    def create_access_token(
        data: dict[str, str | int],
        expires_minutes: int = 15,
    ) -> str:
        """Create a JWT access token.

        Args:
            data: Payload to encode in token.
            expires_minutes: Token expiration time in minutes.

        Returns:
            Encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(
            minutes=expires_minutes
        )
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
