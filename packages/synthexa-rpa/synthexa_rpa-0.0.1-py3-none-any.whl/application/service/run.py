from pydantic.dataclasses import dataclass
from pydantic import Field
from uuid import uuid4

from src.application.service.config import ConfigFactory


@dataclass(slots=True, frozen=True, kw_only=True)
class Run:
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    config: ConfigFactory = Field(...)

    def started(self):
        self.config.orchestrator_gateway.registry_status_run(
            run_id=self.run_id,
            schedule_id=self.config.schedule_id,
            status="started"
        )

    def aborted(self):
        self.config.orchestrator_gateway.registry_status_run(
            run_id=self.run_id,
            schedule_id=self.config.schedule_id,
            status="aborted"
        )

    def finished(self):
        self.config.orchestrator_gateway.registry_status_run(
            run_id=self.run_id,
            schedule_id=self.config.schedule_id,
            status="finished"
        )
