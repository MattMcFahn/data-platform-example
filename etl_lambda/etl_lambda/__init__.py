"""Expose application settings for the package"""

from dotenv import load_dotenv  # type: ignore

from etl_lambda.config import get_settings

load_dotenv(".env")
remediation_settings = get_settings()
