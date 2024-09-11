from abc import ABC, abstractmethod
from dataclasses import dataclass

from uncountable.core.async_batch import AsyncBatchProcessor
from uncountable.core.client import Client
from uncountable.integration.telemetry import JobLogger
from uncountable.types import webhook_job_t
from uncountable.types.job_definition_t import JobDefinition, JobResult, ProfileMetadata


@dataclass(kw_only=True)
class JobArgumentsBase:
    job_definition: JobDefinition
    profile_metadata: ProfileMetadata
    client: Client
    batch_processor: AsyncBatchProcessor
    logger: JobLogger


@dataclass(kw_only=True)
class CronJobArguments(JobArgumentsBase):
    pass


@dataclass(kw_only=True)
class WebhookJobArguments(JobArgumentsBase):
    payload: webhook_job_t.WebhookEventBody


JobArguments = CronJobArguments | WebhookJobArguments


class Job(ABC):
    _unc_job_registered: bool = False

    @abstractmethod
    def run_outer(self, args: JobArguments) -> JobResult: ...


class CronJob(Job):
    def run_outer(self, args: JobArguments) -> JobResult:
        assert isinstance(args, CronJobArguments)
        return self.run(args)

    @abstractmethod
    def run(self, args: CronJobArguments) -> JobResult: ...


class WebhookJob(Job):
    def run_outer(self, args: JobArguments) -> JobResult:
        assert isinstance(args, WebhookJobArguments)
        return self.run(args)

    @abstractmethod
    def run(self, args: WebhookJobArguments) -> JobResult: ...


def register_job(cls: type[Job]) -> type[Job]:
    cls._unc_job_registered = True
    return cls
