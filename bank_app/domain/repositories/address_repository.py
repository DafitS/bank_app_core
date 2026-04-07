
from abc import ABC, abstractmethod

from sqlalchemy import UUID

from bank_app.domain.entities.address import Address


class AddressRepository(ABC):

    @abstractmethod
    def create(self, address: Address) -> Address:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, address_id: UUID) -> Address:
        raise NotImplementedError

    @abstractmethod
    def update(self, address: Address) -> Address:
        raise NotImplementedError

    @abstractmethod
    def delete(self, address: Address) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: str):
        raise NotImplementedError
