from contextlib import contextmanager
import re, os
import exceptions as ex
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound
from orm import Accounts, Users, Transactions
from utils import generate_unique_account_number
from passlib.context import CryptContext




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
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError("User does not exist")

            account_number = generate_unique_account_number()
            account = Accounts(
                account_number=account_number,
                user_id=user_id
            )
            session.add(account)
            session.flush()
            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "user_id": user_id, "amount": account.amount
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
                }
                for acc in accounts
            ]


    def delete_account(self, number):
        with self.get_session() as session:
            account = session.query(Accounts).filter_by(account_number=number).one_or_none()
            if account is None:
                raise ex.NotFoundError(f"Account {number} not found")
            session.delete(account)

    def create_user(self, email):
        with self.get_session() as session:
          
            user = Users(email=email)
            session.add(user)
            session.flush() 
            new_account_number = generate_unique_account_number()
            account = Accounts(
                account_number=new_account_number,
                user_id = user.user_id
            )
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
            result = []
            for u in users:
                result.append({
                    "id": u.user_id,
                    "email": u.email,
                    "account_id": u.accounts[0].account_id if u.accounts else None
                })
            return result 
        
    def delete_user(self, user_id):
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError(f"User {user_id} not found")
            session.delete(user)

    def update_account(self, number, new_amount):
        if not isinstance(new_amount, (int, float)):
            raise ex.ErrorConversionType("Amount must be a number!")
        if new_amount < 0:
            raise ex.AmountTooSmallError("Amount must be greater than 0!")

        with self.get_session() as session:
            account = session.query(Accounts).filter_by(account_number=number).first()
            if account is None:
                raise ex.NotFoundError(f"Account {number} not found")

            account.amount = new_amount
            session.flush()

            return {
                "account_id": account.account_id,
                "account_number": account.account_number,
                "amount": account.amount,
                "user_id": account.user_id
            }


    def update_user(self, user_id, new_email):
        
        with self.get_session() as session:
            user = session.query(Users).filter_by(user_id=user_id).one_or_none()
            if user is None:
                raise ex.NotFoundError(f"User {user_id} not found")

            existing_email = session.query(Users).filter_by(email=new_email).one_or_none()
            if existing_email and existing_email.user_id != user_id:
                raise ex.DuplictedError("Email already in use!")

            user.email = new_email
            session.flush()

            return {
                "id": user.user_id,
                "email": user.email
            }

        
    def create_transaction(self, account_from_id, account_to_id, amount):
        if account_from_id == account_to_id:
            raise ex.ErrorConversionType("The same account number!")

        if amount <= 0:
            raise ex.AmountTooSmallError("Amount must be greater than 0!")

        with self.get_session() as session:
            account_from = session.query(Accounts).filter_by(account_id=account_from_id).one_or_none()
            if account_from is None:
                raise ex.NotFoundError(f"Account {account_from_id} not exist!")

            account_to = session.query(Accounts).filter_by(account_id=account_to_id).one_or_none()
            if account_to is None:
                raise ex.NotFoundError(f"Account {account_to_id} not exist!")

            if account_from.amount < amount:
                raise ex.AmountTooSmallError("Too little deposit in account!")

            account_from.amount -= amount
            account_to.amount += amount

            transaction = Transactions(
                account_id_from=account_from_id,
                account_id_to=account_to_id,
                amount=amount
            )

            session.add(transaction)
            session.flush()
            return {
                "transaction_id": transaction.transaction_id,
                "account_from_id": account_from_id,
                "account_to_id": account_to_id,
                "amount": amount
            }


#pon 16 dodac secret, instal cicd z pytontml pyprojecttoml.