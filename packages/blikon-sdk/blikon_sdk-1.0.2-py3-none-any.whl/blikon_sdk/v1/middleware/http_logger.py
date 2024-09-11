import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable
from blikon_sdk.v1.models.http_log_model import HttpLog
from blikon_sdk.v1.core.setup import verify_blikon_sdk_initialized
from blikon_sdk.v1.services.log_service import LogService
from blikon_sdk.v1.utils.utils import DateTimeUtil
from datetime import datetime


class HttpLoggingMiddleware(BaseHTTPMiddleware):

    IGNORED_ENDPOINTS = ["/docs", "/openapi.json"]

    def __init__(self, app):
        super().__init__(app)
        self.log_service = LogService()
        # Verificar que el blikon_sdk esté inicializado.
        verify_blikon_sdk_initialized()

    async def dispatch(self, request: Request, call_next: Callable):


        start_datetime = datetime.now()
        user_agent = request.headers.get("user-agent", "")
        os_info, browser = self._parse_user_agent(user_agent)
        # Leer el cuerpo de la solicitud
        body = await request.body()
        # Procesar la solicitud
        response: Response = await call_next(request)

        # Procesar el cuerpo de la respuesta
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        end_datetime = datetime.now()
        process_time = end_datetime - start_datetime
        status_code = response.status_code

        # Obtener los cuerpos de la solicitud y la respuesta
        MAX_LOG_BODY_SIZE = 1000
        request_body_clean = self._get_request_body(body)[:MAX_LOG_BODY_SIZE]
        response_body_clean = self._get_response_body(response_body)[:MAX_LOG_BODY_SIZE]

        # Construir el objeto del http log
        http_log = HttpLog(
            endpoint=request.url.path,
            method=request.method,
            start_time=DateTimeUtil.get_datetime_str(start_datetime),
            client_ip=request.client.host,
            real_client_ip=self._get_real_client_ip(request),
            user_agent=user_agent,
            operating_system=os_info,
            browser=browser,
            request_body=request_body_clean,
            end_time=DateTimeUtil.get_datetime_str(end_datetime),
            duration=f"{process_time.total_seconds():.4f}",
            status_code=str(status_code),
            response_body=response_body_clean
        )

        # Hacer el log del http log
        if http_log.endpoint not in self.IGNORED_ENDPOINTS:
            self.log_service.http_info(http_log)

        # Reconstruct the response with the original body
        return Response(content=response_body, status_code=status_code, headers=dict(response.headers))


    def _get_request_body(self, body: bytes) -> str:
        request_body_str = None
        try:
            request_body_str = body.decode('utf-8')
            # Intentar cargar el JSON y luego convertirlo en una cadena limpia
            request_body_json = json.loads(request_body_str)
            request_body_clean = json.dumps(request_body_json, separators=(',', ':'), ensure_ascii=False)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Si falla, mantener el cuerpo en formato texto crudo
            request_body_clean = request_body_str
        return request_body_clean


    def _get_response_body(self, response_body: bytes) -> str:
        try:
            response_body_str = response_body.decode("utf-8")
            # Intentar convertir la respuesta a JSON limpio
            try:
                response_body_json = json.loads(response_body_str)
                response_body_clean = json.dumps(response_body_json, separators=(',', ':'), ensure_ascii=False)
            except json.JSONDecodeError:
                # No es JSON, mantén el cuerpo como está
                response_body_clean = response_body_str
        except UnicodeDecodeError:
            response_body_clean = ""
        return response_body_clean

    def _get_real_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # Verifica si la IP es válida (ej. no es vacía)
            real_ip = forwarded_for.split(',')[0].strip()
            if real_ip:
                return real_ip
        return request.client.host


    def _parse_user_agent(self, user_agent: str):
        os_info = "Unknown OS"
        browser_info = "Unknown Browser"

        # Simple regex patterns (can be improved)
        os_patterns = {
            "Windows": "Windows",
            "Macintosh": "Mac OS",
            "Linux": "Linux",
            "Android": "Android",
            "iPhone": "iOS",
        }

        browser_patterns = {
            "Firefox": "Firefox",
            "Chrome": "Chrome",
            "Safari": "Safari",
            "MSIE": "Internet Explorer",
            "Trident": "Internet Explorer",
        }

        for key, value in os_patterns.items():
            if key in user_agent:
                os_info = value
                break

        for key, value in browser_patterns.items():
            if key in user_agent:
                browser_info = value
                break

        return os_info, browser_info