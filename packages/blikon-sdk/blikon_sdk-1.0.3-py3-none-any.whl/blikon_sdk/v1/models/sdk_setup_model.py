from pydantic import BaseModel


class SDKSetupSettings(BaseModel):
    client_application_name: str = ""
    client_application_version: str
    client_application_mode: int = 0
    log_to_file: bool = False
    logging_level_console: int = 20 # INFO, WARNING, ERROR, CRITICAL
    logging_level_file: int = 20 # INFO, WARNING, ERROR, CRITICAL
