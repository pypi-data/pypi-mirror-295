import sqlite3
import time

from premsql.executors.base import BaseExecutor


class SQLiteExecutor(BaseExecutor):
    def execute_sql(self, sql: str, dsn_or_db_path: str) -> dict:
        conn = sqlite3.connect(dsn_or_db_path)
        cursor = conn.cursor()

        start_time = time.time()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            error = None
        except Exception as e:
            result = None
            error = str(e)

        end_time = time.time()
        cursor.close()
        conn.close()

        result = {
            "result": result,
            "error": error,
            "execution_time": end_time - start_time,
        }
        return result
