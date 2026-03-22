from sqlalchemy.orm import Session
from uuid import UUID
from bank_app.domain.entities.user import User
from bank_app.domain.entities.address import Address
from bank_app.domain.repositories.address_repository import AddressRepository
from bank_app.infrastructure.orm.address import Addresses

class SqlAlchemyAddressRepository(AddressRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, address: Address) -> Address:
        orm = Addresses(
            user_id=address.user_id,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code
        )
        self.session.add(orm)
        self.session.flush()
        return Address(
            address_id=orm.address_id,
            user_id=orm.user_id,
            street=orm.street,
            city=orm.city,
            state=orm.state,
            zip_code=orm.zip_code
        )

    def get_by_id(self, address_id: UUID) -> Address:
        orm = self.session.query(Addresses).filter_by(address_id=address_id).one_or_none()
        if not orm:
            return None
        return Address(
            address_id=orm.address_id,
            user_id=orm.user_id,
            street=orm.street,
            city=orm.city,
            state=orm.state,
            zip_code=orm.zip_code
        )

    def update(self, address: Address) -> Address:
        orm = self.session.query(Addresses).filter_by(address_id=address.address_id).one_or_none()
        if not orm:
            return None
        orm.street = address.street
        orm.city = address.city
        orm.state = address.state
        orm.zip_code = address.zip_code
        self.session.commit()
        return Address(
            address_id=orm.address_id,
            user_id=orm.user_id,
            street=orm.street,
            city=orm.city,
            state=orm.state,
            zip_code=orm.zip_code
        )

    def delete(self, address: Address) -> None:
        orm = self.session.query(Addresses).filter_by(address_id=address.address_id).one_or_none()
        if orm:
            self.session.delete(orm)

    def get_by_user_id(self, user_id: str):
        orm_list = (
            self.session.query(Addresses)
            .filter_by(user_id=user_id)
            .all()
        )
        return [Address(
            address_id=orm.address_id,
            user_id=orm.user_id,
            street=orm.street,
            city=orm.city,
            state=orm.state,
            zip_code=orm.zip_code
        ) for orm in orm_list]
