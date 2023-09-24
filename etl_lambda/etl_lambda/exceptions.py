"""
 Module recording possible exceptions for the application unrelated to data contents,
 with hooks to ensure standardized logging.
"""
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from logging import getLogger

logger = getLogger(__name__)


class Severity(Enum):
    """Types of logging severity"""

    EXCEPTION = auto()
    WARNING = auto()
    INFO = auto()


class BaseResult(Exception, metaclass=ABCMeta):
    """Abstract class used to control process flow"""

    @property
    @abstractmethod
    def is_full_failure(self) -> bool:
        """
        Boolean to indicate whether this exception causes the application to terminate.

        A missing value (uncaught exception) means this exception can either be for full
        application failure, or just for one specific file
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def log_code(self) -> str:
        """Code used for logging purposes & standardisation"""
        raise NotImplementedError

    @property
    @abstractmethod
    def level(self) -> Severity:
        """Severity used for logging purposes"""
        raise NotImplementedError

    def message(self) -> str:
        """Get the exception message inheriting from the docstring and initialisation message"""
        return self.__doc__ + (f": {self}" if str(self) else "")  # type: ignore

    def log(self, extra: dict) -> None:
        """Log the result appropriately"""
        extra = {**{"logCode": self.log_code, "result": self.__class__.__name__}, **extra}

        if self.level == Severity.EXCEPTION:
            logger.exception(msg=self.message(), extra=extra)

        if self.level == Severity.WARNING:
            logger.warning(msg=self.message(), extra=extra)

        if self.level == Severity.INFO:
            logger.info(msg=self.message(), extra=extra)


class UncaughtException(BaseResult):
    """Uncaught exception"""

    is_full_failure = True
    log_code = "LAMBDA-U000"
    level = Severity.EXCEPTION


class NoObjectsInS3Exception(BaseResult):
    """No files found in the S3 bucket"""

    is_full_failure = True
    log_code = "LAMBDA-E000"
    level = Severity.EXCEPTION


class S3IOException(BaseResult):
    """Exception reading/writing to S3"""

    is_full_failure = True
    log_code = "LAMBDA-E001"
    level = Severity.EXCEPTION


class PostgresAccessException(BaseResult):
    """Unable to connect to Postgres"""

    is_full_failure = True
    log_code = "LAMBDA-E003"
    level = Severity.EXCEPTION


class SnowflakeAccessException(BaseResult):
    """Unable to connect to Snowflake"""

    is_full_failure = True
    log_code = "LAMBDA-E003"
    level = Severity.EXCEPTION
