from pydantic.dataclasses import dataclass
from pydantic import Field

from .config import ConfigFactory


@dataclass(slots=True, frozen=True, kw_only=True)
class Logger:
    run_id: str = Field(...)
    config: ConfigFactory = Field(...)

    def debug(self, message: str):
        print("DEBUG: ", message)
        self.config.orchestrator_gateway.registry_log_level(
            run_id=self.run_id,
            log_level="debug",
            message=message
        )

    def info(self, message: str):
        print("INFO: ", message)
        self.config.orchestrator_gateway.registry_log_level(
            run_id=self.run_id,
            log_level="info",
            message=message
        )

    def warning(self, message: str):
        print("WARNING: ", message)
        self.config.orchestrator_gateway.registry_log_level(
            run_id=self.run_id,
            log_level="warning",
            message=message
        )

    def error(self, message: str):
        print("ERROR: ", message)
        self.config.orchestrator_gateway.registry_log_level(
            run_id=self.run_id,
            log_level="error",
            message=message
        )
