from pydantic import BaseModel


class UserDTORequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserDTOResponse(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    