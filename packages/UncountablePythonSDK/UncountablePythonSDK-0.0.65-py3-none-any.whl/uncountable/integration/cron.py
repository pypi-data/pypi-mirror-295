from dataclasses import dataclass

from pkgs.argument_parser import CachedParser
from uncountable.core.async_batch import AsyncBatchProcessor
from uncountable.integration.construct_client import construct_uncountable_client
from uncountable.integration.executors.executors import execute_job
from uncountable.integration.job import CronJobArguments
from uncountable.integration.telemetry import JobLogger, get_otel_tracer
from uncountable.types.job_definition_t import JobDefinition, ProfileMetadata


@dataclass
class CronJobArgs:
    definition: JobDefinition
    profile_metadata: ProfileMetadata


cron_args_parser = CachedParser(CronJobArgs)


def cron_job_executor(**kwargs: dict) -> None:
    args_passed = cron_args_parser.parse_storage(kwargs)
    with get_otel_tracer().start_as_current_span(name="cron_executor") as span:
        job_logger = JobLogger(
            base_span=span,
            profile_metadata=args_passed.profile_metadata,
            job_definition=args_passed.definition,
        )
        client = construct_uncountable_client(
            profile_meta=args_passed.profile_metadata, job_logger=job_logger
        )
        batch_processor = AsyncBatchProcessor(client=client)
        args = CronJobArguments(
            job_definition=args_passed.definition,
            client=client,
            batch_processor=batch_processor,
            profile_metadata=args_passed.profile_metadata,
            logger=job_logger,
        )

        execute_job(
            args=args,
            profile_metadata=args_passed.profile_metadata,
            job_definition=args_passed.definition,
        )
