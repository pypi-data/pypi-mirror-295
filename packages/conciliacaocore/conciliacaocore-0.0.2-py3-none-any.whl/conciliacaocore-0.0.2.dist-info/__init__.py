from .config import Config
from .database import get_connection, execute_query


def init_package(db_host, db_name, db_user, db_password):
    Config.init_config(db_host, db_name, db_user, db_password)


# Export necessary functions
__all__ = ["init_package", "get_connection", "execute_query"]
