from domain.interfaces.i_auth_repository import IAuthRepository
from infrastructure.config.database import get_connection


class AuthRepository(IAuthRepository):

    def check_login(self, username, password) -> dict | None:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, ref_id FROM [User] WHERE username=? AND password=? AND status='Active'",
                (username, password),
            )
            result = cursor.fetchone()
            conn.close()
            if result:
                return {"role": result[0], "ref_id": result[1]}
            return None
        except Exception:
            return None

    def get_user_by_username(self, username) -> dict | None:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, role, ref_id, status FROM [User] WHERE username=?",
                (username,)
            )
            result = cursor.fetchone()
            conn.close()
            if result:
                return {
                    "user_id": result[0],
                    "username": result[1],
                    "role": result[2],
                    "ref_id": result[3],
                    "status": result[4]
                }
            return None
        except Exception:
            return None
