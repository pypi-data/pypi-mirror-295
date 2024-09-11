from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from typing import Literal
from blikon_sdk.v1.models.sdk_setup_model import SDKSetupSettings
from blikon_sdk.v1.models.sdk_configuration_model import SDKConfiguration

# Construir la ruta del archivo .env en relación al directorio actual
#env_path = Path(__file__).resolve().parent / '.env'
#load_dotenv(dotenv_path=env_path)

# Toma las variables de entorno del .env en el directorio raíz del proyecto
load_dotenv()

# Configuración para uso del SDK
sdk_configuration:  SDKConfiguration

class Settings(BaseSettings):

    API_USER: str = "user"
    API_USER_PASSWORD: str = "password"
    JWT_SECRET: str = "your_jwt_secret"
    JWT_EXPIRATION_TIME_MINUTES: int = 30

    class Config:
        env_prefix = 'SDK_'
        env_file = ".env"
        extra = 'allow'  # Permite variables adicionales

sdk_settings = Settings()
sdk_configuration = SDKConfiguration()

def set_client_application_settings(setup: SDKSetupSettings) -> SDKConfiguration:
    global sdk_configuration
    sdk_configuration = SDKConfiguration(
        client_application_name=setup.client_application_name,
        client_application_version=setup.client_application_version,
        client_application_mode=setup.client_application_mode,
        log_to_file=setup.log_to_file,
        logging_level_console=setup.logging_level_console,
        logging_level_file=setup.logging_level_file,
    )
    return sdk_configuration


