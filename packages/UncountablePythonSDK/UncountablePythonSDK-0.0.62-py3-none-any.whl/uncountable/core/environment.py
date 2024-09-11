import functools
import os
from importlib.metadata import PackageNotFoundError, version


@functools.cache
def get_version() -> str:
    try:
        version_str = version("UncountablePythonSDK")
    except PackageNotFoundError:
        version_str = "unknown"
    return version_str


def get_integration_env() -> str | None:
    return os.environ.get("UNC_INTEGRATION_ENV")


def get_webhook_server_port() -> int:
    return int(os.environ.get("UNC_WEBHOOK_SERVER_PORT") or 5001)


def get_otel_enabled() -> bool:
    return os.environ.get("UNC_OTEL_ENABLED") == "true"
