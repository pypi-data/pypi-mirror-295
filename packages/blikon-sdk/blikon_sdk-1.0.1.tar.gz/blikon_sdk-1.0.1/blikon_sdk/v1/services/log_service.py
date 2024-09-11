import logging
from blikon_sdk.v1.models.http_log_model import HttpLog
from blikon_sdk.v1.models.error_detail_model import ErrorDetail
from blikon_sdk.v1.utils.utils import DateTimeUtil

sep = " | "
# 100 caracteres
line = "----------------------------------------------------------------------------------------------------"

class LogService():
    def __init__(self):
        pass


    def info(self, text: str):
        logging.info(text)


    def error(self, text: str):
        logging.error(text)
        self._handleLog()


    def error_info(self, error_detail: ErrorDetail):
        self.error(f"{line}")
        self.error(f"Client Application Name: '{error_detail.client_application_name}'")
        self.error(f"Client Application Mode: '{error_detail.client_application_mode}'")
        self.error(f"Datetime: '{DateTimeUtil.get_datetime_str(error_detail.datetime)}'")
        self.error(f"Exception Type: '{error_detail.exception_type}'")
        self.error(f"Error Message: '{error_detail.error_message}'")
        self.error(f"File Name: '{error_detail.file_name}'")
        self.error(f"Function Name: '{error_detail.function_name}'")
        self.error(f"Line Number: '{error_detail.line_number}'")
        self.error(f"Endpoint: '{error_detail.endpoint}'")
        self.error(f"Status Code: '{error_detail.status_code}'")
        self.error(f"Validation Errors: '{error_detail.validation_errors}'")
        self.error(f"{line}")
        self._handleLog()


    def http_info(self, http_log: HttpLog):
        self.info(f"{line}")
        self.info(f"Endpoint: '{http_log.endpoint}'{sep}Starting Time: '{http_log.start_time}'")
        #self.info(f"IP: '{http_log.client_ip}'")
        self.info(f"IP: '{http_log.real_client_ip}'{sep}IO: '{http_log.operating_system}'{sep}Browser: '{http_log.browser}'")
        self.info(f"Request: '{http_log.request_body}'")
        self.info(f"Status Code: '{http_log.status_code}'")
        self.info(f"Response: '{http_log.response_body}'")
        self.info(f"Ending Time: '{http_log.end_time}'{sep}Duration: '{http_log.duration} sec'")
        self.info(f"{line}")
        self._handleLog()


    def _handleLog(self):
        # Aquí se manejará lo referente a los logs.
        # Podrán almacenarse en BD, archivo, o en algún otro medio
        pass


    def service_info(self, service_name: str, function_name: str, key: str, value: str):
        self.info(f"{line}")
        self.info(f"Service: '{service_name}'{sep}Function: '{function_name}'{sep}{key}: '{value}'")
        self.info(f"{line}")
        self._handleLog()


    def service_request_info(self, service_name: str, function_name: str, json: str):
        self.info(f"{line}")
        self.info(f"Service: '{service_name}'{sep}Function: '{function_name}'{sep}Request: '{json}'")
        self.info(f"{line}")
        self._handleLog()


    def service_response_info(self, service_name: str, function_name: str, status_code: int, json: str):
        self.info(f"{line}")
        self.info(f"Service: '{service_name}'{sep}Function: '{function_name}'{sep}Status Code: '{status_code}'{sep}Response: '{json}'")
        self.info(f"{line}")
        self._handleLog()