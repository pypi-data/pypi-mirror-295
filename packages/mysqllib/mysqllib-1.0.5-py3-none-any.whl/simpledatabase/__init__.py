from typing import Optional, Any
import pymysql
import time
from mysqllib.err import DatabaseError

_connection_attempts = 10
_connection_attempts_sleep = 1
_connection = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': '',
    'password': '',
    'database': ''
}


def connect(
        user: str,
        password: str,
        database: str,
        host: str='127.0.0.1',
        port: int=3306
):
    global _connection

    _connection = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database
    }


def get_connection(attempts: Any='auto') -> pymysql.Connection:
    global _connection_attempts, _connection_attempts_sleep, _connection

    if attempts == 'auto':
        attempts = _connection_attempts

    if attempts is not None:
        for attempt in range(attempts):
            try:
                return get_connection(attempts=None)
            except DatabaseError:
                time.sleep(_connection_attempts_sleep)

    try:
        return pymysql.connect(
            host=_connection['host'],
            user=_connection['user'],
            password=_connection['password'],
            database=_connection['database'],
            port=_connection['port']
        )
    except pymysql.MySQLError as e:
        raise DatabaseError(str(e))


def fetchone(query, args=None) -> Optional[dict]:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            row = cursor.fetchone()

            if not row:
                return None

            column_names = [desc[0] for desc in cursor.description]
            return dict(zip(column_names, row))
    except pymysql.MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        connection.close()


def fetchall(query, args=None) -> Optional[list]:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            rows = cursor.fetchall()

            if not rows:
                return None

            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]
    except pymysql.MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        connection.close()


def execute(query, args=None) -> bool:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
        connection.commit()

        return True
    except pymysql.MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        connection.close()
