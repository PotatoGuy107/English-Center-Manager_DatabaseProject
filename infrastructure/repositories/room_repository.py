from domain.interfaces.i_room_repository import IRoomRepository
from infrastructure.config.database import get_connection


class RoomRepository(IRoomRepository):

    @staticmethod
    def get_all_rooms() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT room_id, room_name, capacity, location, status FROM Room")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(room_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT room_id, room_name, capacity, location, status FROM Room WHERE room_id=?", (room_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_next_room_id() -> str:
        """Generate next room_id like R01, R02, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(room_id, 2, LEN(room_id)-1) AS INT)) FROM Room WHERE room_id LIKE 'R%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"R{max_num + 1:02d}"

    @staticmethod
    def insert_room(data) -> int:
        """Insert room. data = (room_name, capacity, location, status). Returns room_id (auto-generated)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Room (room_name, capacity, location, status) 
            OUTPUT INSERTED.room_id
            VALUES (?, ?, ?, ?)
        """, data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update_room(data) -> None:
        """Update room. data = (room_id, room_name, capacity, location, status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Room
            SET room_name=?, capacity=?, location=?, status=?
            WHERE room_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(room_id, new_status) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Room SET status=? WHERE room_id=?", (new_status, room_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_room(room_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Room WHERE room_id=?", (room_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_next_room_id() -> int:
        """Get next available room_id (for display purposes)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ISNULL(MAX(room_id), 0) + 1 FROM Room")
        next_id = cursor.fetchone()[0]
        conn.close()
        return next_id
