import jwt

from app.core import settings
from app.entities import TokenPayload


def create_access_token(token_payload: TokenPayload) -> str:
    encoded_jwt = jwt.encode(token_payload.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_token_payload(token: str) -> TokenPayload:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return TokenPayload(**payload)
