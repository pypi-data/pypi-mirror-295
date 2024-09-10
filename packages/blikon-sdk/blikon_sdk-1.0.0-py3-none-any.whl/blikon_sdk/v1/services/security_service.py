from datetime import datetime, timezone, timedelta
from jose import jwt, ExpiredSignatureError
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional, Tuple
from blikon_sdk.v1.core.config import sdk_settings, sdk_configuration


class CustomHTTPBearer(HTTPBearer):


    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth = request.headers.get("Authorization")
        if not auth:
            self._raise_401_exception("Not authorized")
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "bearer":
                self._raise_401_exception("Invalid authentication scheme")
            return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
        except ValueError:
            self._raise_401_exception("Invalid authorization header format")


    @staticmethod
    def _raise_401_exception(detail: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class SecurityService():

    http_bearer = CustomHTTPBearer()

    def __init__(self):
        self.jwt_secret = sdk_settings.JWT_SECRET
        self.jwt_algorithm = sdk_configuration.jwt_algorithm
        self.jwt_expiration_time_minutes = sdk_configuration.jwt_expiration_time_minutes
        self.user = sdk_settings.API_USER
        self.password = sdk_settings.API_USER_PASSWORD


    def authenticate_user(self, username: str, password: str) -> bool:
        # FALTA MANEJAR BLOQUEO POR INTENTOS
        autenticado = False
        if username == self.user and password == self.password:
            autenticado = True
        return autenticado


    def create_access_token(self, data: dict) -> str:
        expiration = datetime.utcnow() + (timedelta(minutes=self.jwt_expiration_time_minutes))
        data.update({"exp": expiration})
        payload = data.copy()
        encoded_jwt_token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt_token


    async def verify_api_user_token(self, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
        token = credentials.credentials
        decoded_jwt_token = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
        self.check_token_expiration(decoded_jwt_token)
        return decoded_jwt_token


    async def verify_token(self, token: str, id_usuario: int) -> Tuple[bool, Optional[str]]:
        try:
            decoded_token = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                options={"verify_exp": True}
            )

            # Verificar la fecha de expiración
            exp_timestamp = decoded_token.get("exp")
            if exp_timestamp:
                # Convertir timestamp a datetime en UTC (con información de zona horaria)
                exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                # Comparar con la hora actual en UTC (con información de zona horaria)
                current_datetime = datetime.now(tz=timezone.utc)
                if exp_datetime < current_datetime:
                    return False, "Token expirado"

            # Verificar que el token pertenezca al usuario
            if decoded_token.get("sub") != str(id_usuario):
                return False, "El token no pertenece al usuario especificado"

        except ExpiredSignatureError:
            return False, "Token expirado"
        except PyJWTError:
            return False, "Token inválido"

        return True, None


    def check_token_expiration(self, decoded_token: dict):
        if 'exp' not in decoded_token:
            self._raise_401_exception("Token no contiene información de expiración")
        current_time = datetime.now(tz=timezone.utc).timestamp()
        if decoded_token["exp"] < current_time:
            self._raise_401_exception("Token expirado.")


    @staticmethod
    def _raise_401_exception(detail: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
