import psycopg2
from conciliacaocore.config import Config
from conciliacaocore.logger import setup_logger, error

logger = setup_logger(__name__)


def get_connection():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=5432,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
        )
        return conn
    except Exception as e:
        error(logger, f"Error in get_connection: {str(e)}")
        return None


def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        error(logger, "Failed to get database connection")
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        error(logger, f"Error executing query: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
