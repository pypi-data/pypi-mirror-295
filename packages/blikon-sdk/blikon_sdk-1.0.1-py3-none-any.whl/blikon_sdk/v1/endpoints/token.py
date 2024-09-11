from fastapi import APIRouter, HTTPException
from blikon_sdk.v1.services.security_service import SecurityService
from blikon_sdk.v1.schemas.shared_schemas import TokenRequest, TokenResponse, ErrorResponse

router = APIRouter()

@router.post("/token", tags=["token"], response_model=TokenResponse, responses={422: {"model": ErrorResponse}})
async def login_for_access_token(credentials: TokenRequest):
    security_service= SecurityService()
    user_authenticated = security_service.authenticate_user(credentials.username, credentials.password)
    if not user_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Nombre de usuario o contraseña incorrectos"
        )
    token_jwt = security_service.create_access_token(data={"sub": credentials.username})
    api_response = TokenResponse(
        result=True,
        message="Token generado correctamente",
        token=token_jwt,
        token_type="bearer"
    )
    return api_response

