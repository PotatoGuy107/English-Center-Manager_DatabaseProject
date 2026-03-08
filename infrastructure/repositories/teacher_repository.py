import sqlite3
import os

from domain.interfaces.i_teacher_repository import ITeacherRepository
from infrastructure.config.database import DB_PATH


class TeacherRepository(ITeacherRepository):

    @staticmethod
    def get_all() -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id, full_name, specialization, degree, phone_number, status FROM Teacher")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Teacher VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Teacher
            SET full_name=?, specialization=?, degree=?, phone_number=?, status=?
            WHERE teacher_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(teacher_id) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Teacher WHERE teacher_id=?", (teacher_id,))
        conn.commit()
        conn.close()
