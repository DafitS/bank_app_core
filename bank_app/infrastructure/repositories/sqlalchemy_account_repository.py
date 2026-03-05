from sqlalchemy.orm import Session
from bank_app.domain.entities.account import Account
from bank_app.domain.repositories.account_repository import AbstractAccountRepository
from bank_app.infrastructure.orm.account import Accounts
from bank_app.domain.exceptions import NotFoundError
from decimal import Decimal
from datetime import datetime, timezone

class SqlAlchemyAccountRepository(AbstractAccountRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, account: Account) -> Account:
        orm = Accounts(
            account_id=account.account_id,     
            account_number=str(account.account_number),  
            user_id=account.user_id,
            amount=Decimal(account.amount)        
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return Account(
            account_id=orm.account_id,
            account_number=orm.account_number,
            user_id=orm.user_id,
            amount=orm.amount,
            active=orm.active
        )

    def get_by_id(self, account_id: str) -> Account | None:
        orm = self.session.query(Accounts).filter_by(account_id=account_id).one_or_none()
        if not orm:
            return None
        return Account(
            account_id=orm.account_id,
            account_number=orm.account_number,
            user_id=orm.user_id,
            amount=orm.amount,
            active=orm.active
        )

    def get_by_number(self, account_number: str) -> Account | None:
        orm = self.session.query(Accounts).filter_by(account_number=str(account_number)).one_or_none()
        if not orm:
            return None
        return Account(
            account_id=orm.account_id,
            account_number=orm.account_number,
            user_id=orm.user_id,
            amount=orm.amount,
            active=orm.active
        )

    def update(self, account: Account) -> Account:
        orm = self.session.query(Accounts).filter_by(account_id=account.account_id).one()
        orm.amount = account.amount
        self.session.commit()
        return Account(
            account_id=orm.account_id,
            account_number=orm.account_number,
            user_id=orm.user_id,
            amount=orm.amount,
            active=orm.active
        )

    def disable(self, account: Account) -> None:
        try:
            orm = self.session.query(Accounts).filter_by(account_id=account.account_id).one_or_none()

            if not orm:
                raise NotFoundError("Account not found")

            
            orm.active = False
            orm.closed_at = datetime.now(timezone.utc)

            
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    def list_all(self) -> list[Account]:
        orms = self.session.query(Accounts).all()
        return [
            Account(
                account_id=o.account_id,
                account_number=o.account_number,
                user_id=o.user_id,
                amount=o.amount,
                active = o.active
            )
            for o in orms
        ]