from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional, Any


"""
Response de la respuesta genérica de los API de Blikondev
"""
class ApiResponse(BaseModel):
    result: bool
    message: str


"""
Response de los errores de los API de Blikondev
"""
class ErrorResponse(ApiResponse):
    exception_type: str
    validation_errors: Optional[List[Dict[str, Any]]] = None


"""
Request para recibir las credenciales de solicitud de token
"""
class TokenRequest(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not value:
            raise ValueError('El campo es requerido')
        # Verificar longitud del campo
        if not (4 <= len(value) <= 21):
            raise ValueError('El nombre de usuario debe tener de 5 a 20 caracteres')
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if not value:
            raise ValueError('El campo es requerido')
        # Verificar longitud del campo
        if not (4 <= len(value) <= 21):
            raise ValueError('La contraseña debe tener de 5 a 20 caracteres')
        return value


"""
Response al obtenerse el token de acceso JWT
"""
class TokenResponse(ApiResponse):
    token: str
    token_type: str
