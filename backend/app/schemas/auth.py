from pydantic import BaseModel, ConfigDict


class TelegramUserData(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class TelegramAuthRequest(BaseModel):
    init_data: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    subscription_status: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

