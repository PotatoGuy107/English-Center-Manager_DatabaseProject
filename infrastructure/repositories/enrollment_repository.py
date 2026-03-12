"""Repository for Enrollment table operations"""
from infrastructure.config.database import get_connection


class EnrollmentRepository:
    """Manages Enrollment records in SQL Server."""

    @staticmethod
    def get_next_enrollment_id() -> str:
        """Generate next enrollment_id like EN001, EN002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(enrollment_id, 3, LEN(enrollment_id)-2) AS INT)) FROM Enrollment WHERE enrollment_id LIKE 'EN%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"EN{max_num + 1:03d}"

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date, 
                   e.start_date, e.end_date, e.enrollment_status,
                   s.full_name, c.course_name
            FROM Enrollment e
            LEFT JOIN Student s ON e.student_id = s.student_id
            LEFT JOIN Course c ON e.course_id = c.course_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(enrollment_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT enrollment_id, student_id, course_id, enrollment_date, 
                   start_date, end_date, enrollment_status 
            FROM Enrollment WHERE enrollment_id=?
        """, (enrollment_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_by_student(student_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.enrollment_id, e.course_id, c.course_name, e.enrollment_date, 
                   e.start_date, e.end_date, e.enrollment_status
            FROM Enrollment e
            LEFT JOIN Course c ON e.course_id = c.course_id
            WHERE e.student_id=?
        """, (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_course(course_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.enrollment_id, e.student_id, s.full_name, e.enrollment_date, 
                   e.start_date, e.end_date, e.enrollment_status
            FROM Enrollment e
            LEFT JOIN Student s ON e.student_id = s.student_id
            WHERE e.course_id=?
        """, (course_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> str:
        """Insert enrollment. data = (enrollment_id, student_id, course_id, enrollment_date, start_date, end_date, enrollment_status). Returns enrollment_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Enrollment (enrollment_id, student_id, course_id, enrollment_date, start_date, end_date, enrollment_status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update(data) -> None:
        """Update enrollment. data = (enrollment_id, student_id, course_id, enrollment_date, start_date, end_date, enrollment_status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Enrollment
            SET student_id=?, course_id=?, enrollment_date=?, start_date=?, end_date=?, enrollment_status=?
            WHERE enrollment_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[6], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(enrollment_id, status) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Enrollment SET enrollment_status=? WHERE enrollment_id=?", (status, enrollment_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(enrollment_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Enrollment WHERE enrollment_id=?", (enrollment_id,))
        conn.commit()
        conn.close()
