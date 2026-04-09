from bank_app.domain.dto.user_dto import UserDTOResponse
from bank_app.domain.entities.address import Address
from bank_app.domain.entities.user import User


class UserMapper:

    @staticmethod
    def to_dto(user: User, address: Address | None) -> UserDTOResponse:
        return UserDTOResponse(
            user_id=str(user.user_id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            address=(
                {
                    "street": address.street,
                    "city": address.city,
                    "state": address.state,
                    "zip_code": address.zip_code,
                }
                if address else None
            )
        )
