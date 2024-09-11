from .config import Config
from .database import get_connection, execute_query
from .date_utils import parse_java_calendar, parse_java_calendar_date
from .spark import create_spark_session, stop_spark_session
from .logger import setup_logger, debug, info, warning, error, critical


def init_package(db_host, db_name, db_user, db_password):
    Config.init_config(db_host, db_name, db_user, db_password)


__all__ = [
    "init_package",
    "Config",
    "get_connection",
    "execute_query",
    "parse_java_calendar",
    "parse_java_calendar_date",
    "create_spark_session",
    "stop_spark_session",
    "setup_logger",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]
