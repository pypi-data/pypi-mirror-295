from datetime import datetime, timezone, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional, Tuple
from blikon_sdk.v1.core.config import sdk_settings, sdk_configuration
from blikon_sdk.v1.utils.utils import DateTimeUtil


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth = request.headers.get("Authorization")
        if not auth:
            self._raise_401_exception("No autorizado")
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "bearer":
                self._raise_401_exception("Esquema inválido de autenticación")
            return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
        except ValueError:
            self._raise_401_exception("Formato de Header de autorización inválido")


    @staticmethod
    def _raise_401_exception(detail: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class SecurityService():
    def __init__(self):
        self.jwt_secret = sdk_settings.JWT_SECRET
        self.jwt_expiration_time_minutes = sdk_settings.JWT_EXPIRATION_TIME_MINUTES
        self.jwt_algorithm = sdk_configuration.jwt_algorithm

        self.user = sdk_settings.API_USER
        self.password = sdk_settings.API_USER_PASSWORD


    def authenticate_user(self, username: str, password: str) -> bool:
        # FALTA MANEJAR BLOQUEO POR INTENTOS
        autenticado = False
        if username == self.user and password == self.password:
            autenticado = True
        return autenticado


    def create_access_token(self, data: dict) -> str:
        expiration = DateTimeUtil.get_datetime_now() + (timedelta(minutes=self.jwt_expiration_time_minutes))
        data.update({"exp": expiration})
        payload = data.copy()
        encoded_jwt_token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt_token


    def create_timed_access_token(self, data: dict, days: int = 365) -> str:
        # Sumar 5 años a la fecha actual
        expiration = DateTimeUtil.get_datetime_now() + timedelta(days=days)
        data.update({"exp": expiration})
        payload = data.copy()
        encoded_jwt_token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt_token


    def decode_token(self, token: str) -> Optional[dict]:
        try:
            # Decodificar el token JWT sin considerar decha de expiración
            decoded_token = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                options={"verify_exp": False}
            )
        except JWTError:
            return None
        return decoded_token


    async def verify_token(self, token: str) -> Tuple[bool, str, Optional[dict[str, str]]]:
        try:
            # Decodificar el token con verificación de expiración activada
            decoded_token = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                options={"verify_exp": True}
            )
        except JWTError as e:
            if str(e) == "Signature verification failed.":
                return False, "Verificación de firma fallida", None
            elif str(e) == "Signature has expired.":
                return False, "El token ha expirado", None
            else:
                return False, "Token inválido", None
        return True, "El token es válido", decoded_token


    async def verify_authorization(self, credentials: HTTPAuthorizationCredentials = Depends(CustomHTTPBearer())):
        token = credentials.credentials
        valid_token, message, payload = await self.verify_token(token)
        if not valid_token:
            self._raise_401_exception("No autorizado")


    @staticmethod
    def _raise_401_exception(detail: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
