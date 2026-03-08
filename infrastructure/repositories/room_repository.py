import sqlite3

from domain.interfaces.i_room_repository import IRoomRepository
from infrastructure.config.database import DB_PATH


class RoomRepository(IRoomRepository):

    @staticmethod
    def get_all_rooms() -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT room_id, room_name, capacity, type, status FROM Room")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_room(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Room VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(room_id, new_status) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE Room SET status=? WHERE room_id=?", (new_status, room_id))
        conn.commit()
        conn.close()
