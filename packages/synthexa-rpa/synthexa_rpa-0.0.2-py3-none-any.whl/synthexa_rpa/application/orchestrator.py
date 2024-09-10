from pydantic.dataclasses import dataclass
from pydantic import Field
from typing import Callable, Any

from .config import ConfigFactory
from .run import Run
from .logger import Logger


@dataclass(slots=True, kw_only=True)
class Orchestrator:
    config: ConfigFactory = Field(...)
    logger: Logger = Field(init=False)
    __run: Run = Field(init=False)

    def __post_init__(self):
        self.__run = Run(
            config=self.config,
        )
        self.logger = Logger(
            run_id=self.__run.run_id,
            config=self.config,
        )

    def execute(self, func: Callable[..., None], *args: Any, **kwargs: Any):
        self.__run.started()
        self.logger.info(f"Run {self.__run.run_id} started")
        self.logger.info(f"Executing {func.__name__}")
        self.logger.debug(f"Arguments args: {args}")
        self.logger.debug(f"Arguments kwargs: {kwargs}")
        try:
            func(*args, **kwargs)
            self.__run.finished()
            self.logger.info(
                f"Run {self.__run.run_id} finished"
            )
        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.__run.aborted()
            raise
