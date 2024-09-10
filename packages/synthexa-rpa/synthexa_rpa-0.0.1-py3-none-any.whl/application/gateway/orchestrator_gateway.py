from abc import ABC, abstractmethod
from typing import Literal


class OrchestratorGateway(ABC):
    @abstractmethod
    def registry_status_run(
        self,
        run_id: str,
        schedule_id: str,
        status: Literal['started', 'aborted', 'finished'],
    ) -> None:
        ...

    @abstractmethod
    def registry_log_level(
        self,
        run_id: str,
        message: str,
        log_level: Literal['debug', 'info', 'warning', 'error']
    ) -> None:
        ...
