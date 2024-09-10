from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field

from src.application.gateway.orchestrator_gateway import OrchestratorGateway
from src.infra.gateway.orchestrator_gateway.supabase \
    import SupabaseOrchestratorGateway


@dataclass(
    config=ConfigDict(arbitrary_types_allowed=True),
    slots=True,
    kw_only=True
)
class ConfigFactory:
    tenant_id: str = Field(...)
    schedule_id: str = Field(...)
    connection_url: str = Field(...)
    connection_key: str = Field(...)
    login: str = Field(...)
    password: str = Field(...)
    orchestrator_gateway: OrchestratorGateway = Field(init=False)

    def __post_init__(self):
        self.orchestrator_gateway = SupabaseOrchestratorGateway(
            tenant_id=self.tenant_id,
            login=self.login,
            password=self.password,
            supabase_url=self.connection_url,
            supabase_key=self.connection_key
        )
