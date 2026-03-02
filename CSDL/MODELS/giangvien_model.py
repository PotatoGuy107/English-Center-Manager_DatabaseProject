import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "quanlytrungtam.db")


class GiangVienModel:

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id, full_name, specialization, degree, phone_number, status FROM Teacher")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def insert(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Teacher VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Teacher 
            SET full_name=?, specialization=?, degree=?, phone_number=?, status=? 
            WHERE teacher_id=?""",
            (data[1], data[2], data[3], data[4], data[5], data[0])
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(teacher_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Teacher WHERE teacher_id=?", (teacher_id,))
        conn.commit()
        conn.close()
