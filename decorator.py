import sqlite3
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def bd_connection(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('bank.db')
        cursor = connection.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            logger.error(f"Error in {func.__name__}: {e}")
            return f"Error: {e}"
        finally:
            cursor.close()
            connection.close()

    return wrapper


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error in {func.__name__}: {e}')
            return f'Error in {func.__name__}: {e}'
    return wrapper
