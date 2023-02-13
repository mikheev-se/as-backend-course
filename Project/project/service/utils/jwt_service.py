from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from project.core.settings import settings
from project.models.utils.jwt_token import JwtToken
from project.models.utils.payload import Payload
from jose import JWTError, jwt
from project.models.roles import valid_roles
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta

oauth2_schema = OAuth2PasswordBearer('/users/authorize')


class JwtService:

    @staticmethod
    def get_current_user_id(token: str = Depends(oauth2_schema)):
        return JwtService.verify_token(token)

    @staticmethod
    def check_if_admin(token: str = Depends(oauth2_schema)):
        role: valid_roles = JwtService.get_user_role(token)
        if role == 'admin':
            return role
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password, password_hash)

    @staticmethod
    def create_token(id: int, role: valid_roles) -> JwtToken:
        now = datetime.now()
        payload = Payload(
            iat=now,
            exp=now + timedelta(seconds=settings.jwt_expires_sec),
            sub=str(id),
            role=role
        )

        token = jwt.encode(
            payload.dict(),
            settings.jwt_secret,
            settings.jwt_algorithm
        )
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> int | None:
        try:
            payload = Payload(
                **jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[
                        settings.jwt_algorithm
                    ]
                )
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Токен невалиден'
            )

        return payload.sub

    @staticmethod
    def get_user_role(token: str) -> valid_roles | None:
        try:
            payload = Payload(
                **jwt.decode(
                    token,
                    settings.jwt_secret,
                    algorithms=[
                        settings.jwt_algorithm
                    ]
                )
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Токен невалиден'
            )

        return payload.role
