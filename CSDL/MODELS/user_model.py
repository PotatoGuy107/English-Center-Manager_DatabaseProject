import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "quanlytrungtam.db")


class UserModel:

    @staticmethod
    def get_all_students():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, full_name, phone_number, email, status FROM Student"
        )
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_student(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update_student(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student 
            SET full_name=?, phone_number=?, email=?, status=? 
            WHERE student_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_student(student_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id=?", (student_id,))
        conn.commit()
        conn.close()
