import sqlite3

from domain.interfaces.i_auth_repository import IAuthRepository
from infrastructure.config.database import DB_PATH


class AuthRepository(IAuthRepository):

    def __init__(self):
        self._init_account_data()

    def _init_account_data(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Account (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM Account")
        if cursor.fetchone()[0] == 0:
            accounts = [
                ("admin", "123", "admin"),
                ("staff", "123", "staff"),
                ("teacher", "123", "teacher"),
            ]
            cursor.executemany("INSERT INTO Account VALUES (?, ?, ?)", accounts)
        conn.commit()
        conn.close()

    def check_login(self, username, password) -> dict | None:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role FROM Account WHERE username=? AND password=?",
                (username, password),
            )
            result = cursor.fetchone()
            conn.close()
            if result:
                return {"role": result[0]}
            return None
        except Exception:
            return None
