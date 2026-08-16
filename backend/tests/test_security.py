import jwt
import pytest

from app.core.security import create_access_token, decode_access_token


def test_access_token_round_trip() -> None:
    token = create_access_token("3d46410e-3dcc-440b-b131-e542d0513051")
    assert decode_access_token(token) == "3d46410e-3dcc-440b-b131-e542d0513051"


def test_rejects_invalid_token() -> None:
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("not-a-token")

