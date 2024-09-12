import signal
from dataclasses import asdict
from types import TracebackType
from typing import Optional, assert_never

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger
from opentelemetry.trace import get_current_span
from sqlalchemy.engine.base import Engine

from uncountable.integration.cron import CronJobArgs, cron_job_executor
from uncountable.integration.telemetry import Logger
from uncountable.types import base_t
from uncountable.types.client_config_t import ClientConfigOptions
from uncountable.types.job_definition_t import (
    AuthRetrieval,
    CronJobDefinition,
    JobDefinition,
    ProfileMetadata,
    WebhookJobDefinition,
)

_MAX_APSCHEDULER_CONCURRENT_JOBS = 1


class IntegrationServer:
    _scheduler: BaseScheduler
    _engine: Engine
    _server_logger: Logger

    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._scheduler = BackgroundScheduler(
            timezone="UTC",
            jobstores={"default": SQLAlchemyJobStore(engine=engine)},
            executors={"default": ThreadPoolExecutor(_MAX_APSCHEDULER_CONCURRENT_JOBS)},
        )
        self._server_logger = Logger(get_current_span())

    def register_profile(
        self,
        *,
        profile_name: str,
        base_url: str,
        auth_retrieval: AuthRetrieval,
        jobs: list[JobDefinition],
        client_options: Optional[ClientConfigOptions],
    ) -> None:
        for job_defn in jobs:
            profile_metadata = ProfileMetadata(
                name=profile_name,
                auth_retrieval=auth_retrieval,
                base_url=base_url,
                client_options=client_options,
            )
            match job_defn:
                case CronJobDefinition():
                    # Add to ap scheduler
                    job_kwargs = asdict(
                        CronJobArgs(
                            definition=job_defn, profile_metadata=profile_metadata
                        )
                    )
                    try:
                        existing_job = self._scheduler.get_job(job_defn.id)
                    except ValueError as e:
                        self._server_logger.log_warning(
                            f"could not reconstitute job {job_defn.id}: {e}"
                        )
                        self._scheduler.remove_job(job_defn.id)
                        existing_job = None
                    if existing_job is not None:
                        existing_job.modify(
                            name=job_defn.name,
                            kwargs=job_kwargs,
                        )
                        existing_job.reschedule(
                            CronTrigger.from_crontab(job_defn.cron_spec)
                        )
                        if not job_defn.enabled:
                            existing_job.pause()
                        else:
                            existing_job.resume()
                    else:
                        job_opts: dict[str, base_t.JsonValue] = {}
                        if not job_defn.enabled:
                            job_opts["next_run_time"] = None
                        self._scheduler.add_job(
                            cron_job_executor,
                            # IMPROVE: reconsider these defaults
                            max_instances=1,
                            coalesce=True,
                            trigger=CronTrigger.from_crontab(job_defn.cron_spec),
                            name=job_defn.name,
                            id=job_defn.id,
                            kwargs=job_kwargs,
                            **job_opts,
                        )
                case WebhookJobDefinition():
                    pass
                case _:
                    assert_never(job_defn)

    def serve_forever(self) -> None:
        signal.pause()

    def _start_apscheduler(self) -> None:
        self._scheduler.start()

    def _stop_apscheduler(self) -> None:
        self._scheduler.shutdown()

    def __enter__(self) -> "IntegrationServer":
        self._start_apscheduler()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._stop_apscheduler()
