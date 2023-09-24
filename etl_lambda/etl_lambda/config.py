"""Application settings"""

from datetime import datetime
from os import getenv
from typing import Optional
from uuid import uuid4

from pydantic import BaseSettings  # pylint: disable=no-name-in-module


class Settings(BaseSettings):
    """Relevant application settings exposed: https://pydantic-docs.helpmanual.io/usage/settings/"""

    correlation_id: Optional[str] = getenv("CORRELATION_ID")
    job_id: str = f"{datetime.now().strftime('%Y%m%dT%H%M%S')}_{uuid4()}"

    environment: str = getenv("ENVIRONMENT")  # type: ignore
    s3_url: str = getenv("S3_URL")  # type: ignore
    postgres_url = getenv("POSTGRES_URL")
    snowflake_url = getenv("SNOWFLAKE_URL")

    max_pool_connections: int = int(getenv("THREAD_POOL_SIZE", "10"))

    landing_bucket: str = f"data-platform-{getenv('ENVIRONMENT')}-input-data"  # type: ignore
    ingestion_bucket_prefix: str = getenv("INGESTION_BUCKET", "landing")
    output_bucket_prefix: str = getenv("OUTPUT_BUCKET", "processed")
    application_log_level: str = getenv("APPLICATION_LOG_LEVEL", "INFO")


def get_settings(**kwargs) -> Settings:
    """Get application settings"""
    return Settings(**kwargs)
