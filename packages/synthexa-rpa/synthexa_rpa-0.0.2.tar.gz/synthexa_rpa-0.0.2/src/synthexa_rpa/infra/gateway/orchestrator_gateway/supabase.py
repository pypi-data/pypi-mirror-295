from typing import Literal
from contextlib import contextmanager
from supabase import create_client, Client
from datetime import datetime

from ....application.gateway.orchestrator_gateway import OrchestratorGateway

STATUS_MAP = {"started": 0, "aborted": 1, "finished": 2}
LOG_LEVEL_MAP = {"debug": 0, "info": 1, "warning": 2, "error": 3}


class SupabaseOrchestratorGateway(OrchestratorGateway):
    def __init__(
        self,
        tenant_id: str,
        login: str,
        password: str,
        supabase_url: str,
        supabase_key: str
    ):
        self.tenant_id = tenant_id
        self.login = login
        self.password = password
        self.client: Client = create_client(
            supabase_url=supabase_url,
            supabase_key=supabase_key
        )

    @contextmanager
    def authenticated_session(self):
        """Context manager to handle sign-in and sign-out automatically."""
        try:
            self.__sign_in()
            yield
        except Exception as e:
            raise e
        finally:
            self.__sign_out()

    def __sign_in(self):
        try:
            self.client.auth.sign_in_with_password(
                {
                    "email": self.login,
                    "password": self.password
                }
            )
        except Exception as e:
            raise e

    def __sign_out(self):
        try:
            self.client.auth.sign_out()
        except Exception as e:
            raise e

    def registry_status_run(
        self,
        run_id: str,
        schedule_id: str,
        status: Literal['started', 'aborted', 'finished'],
    ) -> None:
        if status not in STATUS_MAP:
            raise ValueError(f"Invalid status: {status}")

        with self.authenticated_session():
            try:
                if status == "started":
                    self.client.table("runs").insert(  # type: ignore
                        {
                            "id": run_id,
                            "tenant_id": self.tenant_id,
                            "schedule_id": schedule_id,
                            "status": STATUS_MAP[status],
                            "created_by": self.login,
                            "created_at": str(datetime.now())
                        }
                    ).execute()
                else:
                    self.client.table("runs").update(  # type: ignore
                        {
                            "status": STATUS_MAP[status],
                            "updated_by": self.login,
                            "updated_at": str(datetime.now())
                        }
                    ).eq("id", run_id).execute()

            except Exception as e:
                raise e

    def registry_log_level(
        self,
        run_id: str,
        message: str,
        log_level: Literal['debug', 'info', 'warning', 'error']
    ) -> None:
        if log_level not in LOG_LEVEL_MAP:
            raise ValueError(f"Invalid log level: {log_level}")

        with self.authenticated_session():
            try:
                self.client.table("logs").insert(  # type: ignore
                    {
                        "tenant_id": self.tenant_id,
                        "run_id": run_id,
                        "message": message,
                        "level": LOG_LEVEL_MAP[log_level],
                        "created_by": self.login,
                    }
                ).execute()
            except Exception as e:
                raise e
