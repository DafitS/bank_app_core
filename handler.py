from contextlib import contextmanager
import os
import exceptions as ex
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound
from orm import Accounts, Users, Transactions
from utils import generate_unique_account_number, pwd_context
from datetime import datetime

from validations_models import (
    CreateUser as CreateUserValidator,
    CreateAccount as CreateAccountValidator,
    UpdateUser as UpdateUserValidator,
    UpdateAccount as UpdateAccountValidator,
    CreateTransaction as CreateTransactionValidator
)


class BankAppHandler:
    def __init__(self):
        value = os.getenv("URL")
        self.engine = create_engine(value)
        self.session = sessionmaker(bind=self.engine, expire_on_commit=False)

    @contextmanager
    def get_session(self):
        session = self.session()
        try:
            yield session
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise ex.DuplictedError("Record Already Exist!") from e
        except NoResultFound as e:
            session.rollback()
            raise ex.NotFoundError("Record Not Found!") from e
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_account(self, user_id):
        data = CreateAccountValidator(user_id=user_id)
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=data.user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError("User does not exist")
            account_number = generate_unique_account_number()
            account = Accounts(account_number=account_number, user_id=data.user_id)
            session.add(account)
            session.flush()
            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "user_id": data.user_id,
                "amount": account.amount
            }

    def get_accounts(self):
        with self.get_session() as session:
            accounts = session.query(Accounts).all()
            return [
                {
                    "account_id": acc.account_id,
                    "account_number": acc.account_number,
                    "amount": acc.amount,
                    "user_id": acc.user_id
                } for acc in accounts
            ]

    def delete_account(self, number):
        with self.get_session() as session:
            account = session.query(Accounts).filter_by(account_number=number).one_or_none()
            if account is None:
                raise ex.NotFoundError(f"Account {number} not found")
            session.delete(account)

    def create_user(self, email, password):
        user_data = CreateUserValidator(email=email, password=password)
        hashed_password = pwd_context.hash(user_data.password)
        with self.get_session() as session:
            user = Users(email=user_data.email, password=hashed_password)
            session.add(user)
            session.flush()
            account_number = generate_unique_account_number()
            account = Accounts(account_number=account_number, user_id=user.user_id)
            session.add(account)
            session.flush()
            return {
                "id": user.user_id,
                "email": user.email,
                "account_id": account.account_id
            }

    def get_users(self):
        with self.get_session() as session:
            users = session.query(Users).all()
            return [
                {
                    "id": u.user_id,
                    "email": u.email,
                    "account_id": u.accounts[0].account_id if u.accounts else None
                } for u in users
            ]

    def delete_user(self, user_id):
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError(f"User {user_id} not found")
            session.delete(user)

    def update_account(self, number, new_amount):
        data = UpdateAccountValidator(number=number, new_amount=new_amount)
        with self.get_session() as session:
            account = session.query(Accounts).filter_by(account_number=data.number).one_or_none()
            if account is None:
                raise ex.NotFoundError(f"Account {data.number} not found")
            account.amount = data.new_amount
            session.flush()
            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "amount": account.amount,
                "user_id": account.user_id
            }

    def update_user(self, user_id, new_email):
        data = UpdateUserValidator(user_id=user_id, new_email=new_email)
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=data.user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError(f"User {data.user_id} not found")
            existing_email = session.query(Users).filter_by(email=data.new_email).one_or_none()
            if existing_email and existing_email.user_id != data.user_id:
                raise ex.DuplictedError("Email already in use!")
            user.email = data.new_email
            session.flush()
            return {"id": user.user_id, "email": user.email}

    def create_transaction(self, account_from_id, account_to_id, amount):
        data = CreateTransactionValidator(
            account_from=account_from_id,
            account_to=account_to_id,
            amount=amount,
            date=datetime.now()
        )
        with self.get_session() as session:
            acc_from = session.query(Accounts).filter_by(account_id=data.account_from).one_or_none()
            acc_to = session.query(Accounts).filter_by(account_id=data.account_to).one_or_none()
            if not acc_from:
                raise ex.NotFoundError(f"Account {data.account_from} not exist!")
            if not acc_to:
                raise ex.NotFoundError(f"Account {data.account_to} not exist!")
            if acc_from.amount < data.amount:
                raise ex.AmountTooSmallError("Too little deposit in account!")
            acc_from.amount -= data.amount
            acc_to.amount += data.amount
            transaction = Transactions(
                account_id_from=data.account_from,
                account_id_to=data.account_to,
                amount=data.amount
            )
            session.add(transaction)
            session.flush()
            return {
                "transaction_id": transaction.transaction_id,
                "account_from_id": data.account_from,
                "account_to_id": data.account_to,
                "amount": data.amount
            }
