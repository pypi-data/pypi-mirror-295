import traceback, os
from pydantic import ValidationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from blikon_sdk.v1.core.setup import verify_blikon_sdk_initialized
from blikon_sdk.v1.schemas.shared_schemas import ErrorResponse
from blikon_sdk.v1.models.error_detail_model import ErrorDetail
from blikon_sdk.v1.services.log_service import LogService
from blikon_sdk.v1.utils.utils import DateTimeUtil
from blikon_sdk.v1.core.config import sdk_configuration
from typing import List, Dict, Any


class ErrorHandlingMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.log_service = LogService()
        self.setup()
        verify_blikon_sdk_initialized()

    def setup(self):
        @self.app.exception_handler(RequestValidationError)
        @self.app.exception_handler(ValidationError)
        async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
            validation_errors = None
            if isinstance(exc, (RequestValidationError, ValidationError)):
                validation_errors = self._format_and_clean_validation_errors(exc.errors())
                message = "Error de validación"
            else:
                message = "Error interno de servidor"
            return await self._handleError(422, request, message, exc, validation_errors)

        @self.app.exception_handler(HTTPException)
        async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
            return await self._handleError(exc.status_code, request, exc.detail, exc)

        @self.app.exception_handler(Exception)
        async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
            validation_errors = None
            if isinstance(exc, ValidationError):
                validation_errors = self._format_and_clean_validation_errors(exc.errors())
                message = "Error de validación"
            else:
                message = "Error interno de servidor"
            return await self._handleError(500, request, message, exc, validation_errors)

    async def _handleError(self, status_code: int, request: Request, message: str, exc,
                           validation_errors=None) -> JSONResponse:
        file_name, function_name, line_number = self._get_traceback_details(exc)



        error_detail = ErrorDetail(
            client_application_name=sdk_configuration.client_application_name,
            client_application_mode=sdk_configuration.client_application_mode,
            datetime=DateTimeUtil.get_datetime_now(),
            exception_type=type(exc).__name__,
            error_message=str(exc),
            file_name=file_name,
            function_name=function_name,
            line_number=line_number,
            endpoint=str(request.url.path),
            status_code=status_code,
            validation_errors=validation_errors,
        )
        error_response = ErrorResponse(
            result=False,
            message=message,
            exception_type=error_detail.exception_type,
            validation_errors=validation_errors
        )

        # Aquí se hace el log del error
        self.log_service.error_info(error_detail)

        return JSONResponse(
            status_code=status_code,
            content=error_response.model_dump()
        )

    def _get_traceback_details(self, exc: Exception) -> (str, str, int):
        file_name = "unknown"
        function_name = "unknown"
        line_number = -1
        try:
            tb = exc.__traceback__
            tb_frame = traceback.extract_tb(tb)[-1]
            file_name = os.path.basename(tb_frame.filename)
            function_name = tb_frame.name
            line_number = tb_frame.lineno
        except Exception:
            pass
        return file_name, function_name, line_number

    def _format_and_clean_validation_errors(self, validation_errors: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        formatted_errors = []
        for error in validation_errors:
            field = ".".join(str(loc) for loc in error.get('loc', []))
            field = field.replace('body.', '')
            message = error.get('msg', 'Unknown error')
            if message.startswith("Value error, "):
                message = message[len("Value error, "):]
            if message == 'Field required':
                message = "El campo es requerido"
            formatted_errors.append({
                'field': field,
                'message': message
            })
        return formatted_errors