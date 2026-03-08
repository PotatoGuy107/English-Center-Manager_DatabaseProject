"""Repository for Class_Enrollment table operations"""
from infrastructure.config.database import get_connection


class ClassEnrollmentRepository:
    """Manages Class_Enrollment records in SQL Server."""

    @staticmethod
    def get_next_class_enrollment_id() -> str:
        """Generate next class_enrollment_id like CE001, CE002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(class_enrollment_id, 3, LEN(class_enrollment_id)-2) AS INT)) FROM Class_Enrollment WHERE class_enrollment_id LIKE 'CE%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"CE{max_num + 1:03d}"

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.class_enrollment_id, ce.student_id, ce.class_id, ce.join_date, ce.status,
                   s.full_name, c.class_name
            FROM Class_Enrollment ce
            LEFT JOIN Student s ON ce.student_id = s.student_id
            LEFT JOIN Class c ON ce.class_id = c.class_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(class_enrollment_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT class_enrollment_id, student_id, class_id, join_date, status 
            FROM Class_Enrollment WHERE class_enrollment_id=?
        """, (class_enrollment_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_by_class(class_id) -> list:
        """Get all students enrolled in a class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.class_enrollment_id, ce.student_id, s.full_name, s.phone_number, 
                   s.email, ce.join_date, ce.status
            FROM Class_Enrollment ce
            LEFT JOIN Student s ON ce.student_id = s.student_id
            WHERE ce.class_id=?
        """, (class_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_student(student_id) -> list:
        """Get all classes a student is enrolled in"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.class_enrollment_id, ce.class_id, c.class_name, ce.join_date, ce.status
            FROM Class_Enrollment ce
            LEFT JOIN Class c ON ce.class_id = c.class_id
            WHERE ce.student_id=?
        """, (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> str:
        """Insert class enrollment. data = (class_enrollment_id, student_id, class_id, join_date, status). Returns class_enrollment_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Class_Enrollment (class_enrollment_id, student_id, class_id, join_date, status) 
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update_status(class_enrollment_id, status) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Class_Enrollment SET status=? WHERE class_enrollment_id=?", (status, class_enrollment_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(class_enrollment_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Class_Enrollment WHERE class_enrollment_id=?", (class_enrollment_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_by_student_class(student_id, class_id) -> None:
        """Remove a student from a class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Class_Enrollment WHERE student_id=? AND class_id=?", (student_id, class_id))
        conn.commit()
        conn.close()

    @staticmethod
    def check_exists(student_id, class_id) -> bool:
        """Check if student is already enrolled in class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Class_Enrollment WHERE student_id=? AND class_id=?", (student_id, class_id))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
