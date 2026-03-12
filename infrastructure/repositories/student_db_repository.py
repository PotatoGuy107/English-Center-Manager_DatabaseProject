from infrastructure.config.database import get_connection


class StudentDbRepository:
    """Manages Student records in SQL Server."""

    @staticmethod
    def get_next_student_id() -> str:
        """Generate next student_id like ST001, ST002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(student_id, 3, LEN(student_id)-2) AS INT)) FROM Student WHERE student_id LIKE 'ST%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"ST{max_num + 1:03d}"

    @staticmethod
    def get_all_students() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status FROM Student"
        )
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_student_by_id(student_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status FROM Student WHERE student_id=?",
            (student_id,)
        )
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert_student(data) -> int:
        """Insert student. data = (full_name, date_of_birth, gender, address, phone_number, email, register_date, status). Returns student_id (auto-generated)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (full_name, date_of_birth, gender, address, phone_number, email, register_date, status) 
            OUTPUT INSERTED.student_id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update_student(data) -> None:
        """Update student. data = (student_id, full_name, date_of_birth, gender, address, phone_number, email, status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET full_name=?, date_of_birth=?, gender=?, address=?, phone_number=?, email=?, status=?
            WHERE student_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_student(student_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id=?", (student_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_students(keyword) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, full_name, phone_number, email, status FROM Student WHERE full_name LIKE ? OR CAST(student_id AS VARCHAR) LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_students_by_class(class_id) -> list:
        """Get students enrolled in a specific class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.student_id, s.full_name, s.date_of_birth, s.gender, s.phone_number, s.email
            FROM Student s
            JOIN Class_Enrollment ce ON s.student_id = ce.student_id
            WHERE ce.class_id = ?
        """, (class_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_next_student_id() -> int:
        """Get next available student_id (for display purposes)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ISNULL(MAX(student_id), 0) + 1 FROM Student")
        next_id = cursor.fetchone()[0]
        conn.close()
        return next_id
