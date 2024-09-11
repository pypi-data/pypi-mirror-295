import logging
from blikon_sdk.v1.core.config import sdk_settings
from blikon_sdk.v1.core.config import set_client_application_settings
from blikon_sdk.v1.models.sdk_setup_model import SDKSetupSettings
from blikon_sdk.v1.models.sdk_configuration_model import SDKConfiguration


blikon_sdk_setup_initiated = False


def setup_blikon_sdk(app, sdk_setup_settings: SDKSetupSettings):
    # Guardar nombre y modo de la aplicación cliente
    sdk_configuration = set_client_application_settings(sdk_setup_settings)

    # Inicializar la configuración del logging
    _setup_logging(sdk_configuration)

    # Indicar que el SDK ya se ha inicializado
    global blikon_sdk_setup_initiated
    if not blikon_sdk_setup_initiated:
        blikon_sdk_setup_initiated = True


def verify_blikon_sdk_initialized():
    if not blikon_sdk_setup_initiated:
        raise RuntimeError("Blikon SDK no inicializado")


def _setup_logging(sdk_configuration: SDKConfiguration):
    # Desactivar logs del servidor
    # logging.getLogger("uvicorn.error").disabled = True
    # logging.getLogger("uvicorn.access").disabled = True
    # logging.getLogger("fastapi").disabled = True
    # logging.getLogger("starlette").disabled = True

    # Configuración del logger para archivo
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(sdk_configuration.logging_level_file)

    # Configuración del logger para terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(sdk_configuration.logging_level_console)

    if sdk_configuration.log_to_file:
        logging.basicConfig(
            level=sdk_configuration.logging_level_console,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[console_handler, file_handler]
        )
    else:
        logging.basicConfig(
            level=sdk_configuration.logging_level_console,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[console_handler]
        )





