from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Any
from datetime import datetime


class AuthenticatedUser(BaseModel):
    # Valores directos de Blikon API:
    id_usuario: int
    id_perfil_blikon: int
    id_blikon: str
    id_tipo_usuario: int
    id_estatus: int
    usuario_regisrado: bool
    telefono: str
    email: EmailStr
    nombre_perfil: str
    nombre: str
    foto: str
    nombre_usuario: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    # Valores locales de control de usuarios:
    session_token: str
    token_type: str
    created_at: datetime
    last_logged_at: datetime
    failed_login_attempts: int = 0
    blocked: bool
    blocked_at: Optional[datetime]