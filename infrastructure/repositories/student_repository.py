from domain.entities.student_entity import Student
from domain.interfaces.i_student_repository import IStudentRepository
from infrastructure.config.database import get_connection


class StudentRepository(IStudentRepository):
    """Repository for student queries used by Teacher module - connects to SQL Server."""

    def get_students_by_class(self, class_id) -> list:
        """Get students enrolled in a specific class via Class_Enrollment table"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.student_id, s.full_name, s.date_of_birth, s.gender,
                   s.address, s.phone_number, s.email, s.register_date, s.status
            FROM Student s
            INNER JOIN Class_Enrollment ce ON s.student_id = ce.student_id
            WHERE ce.class_id = ?
        """, (class_id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            Student(
                student_id=r[0],
                full_name=r[1],
                date_of_birth=r[2],
                gender=r[3],
                address=r[4],
                phone_number=r[5],
                email=r[6],
                register_date=r[7],
                status=r[8],
            )
            for r in rows
        ]

    def search_students(self, class_id, keyword) -> list:
        """Search students in a class by name or ID"""
        conn = get_connection()
        cursor = conn.cursor()
        kw = f"%{keyword}%"
        cursor.execute("""
            SELECT s.student_id, s.full_name, s.date_of_birth, s.gender,
                   s.address, s.phone_number, s.email, s.register_date, s.status
            FROM Student s
            INNER JOIN Class_Enrollment ce ON s.student_id = ce.student_id
            WHERE ce.class_id = ?
              AND (s.full_name LIKE ? OR CAST(s.student_id AS NVARCHAR) LIKE ?)
        """, (class_id, kw, kw))
        rows = cursor.fetchall()
        conn.close()
        return [
            Student(
                student_id=r[0],
                full_name=r[1],
                date_of_birth=r[2],
                gender=r[3],
                address=r[4],
                phone_number=r[5],
                email=r[6],
                register_date=r[7],
                status=r[8],
            )
            for r in rows
        ]

    def add_student(self, student) -> None:
        pass

    def update_student(self, student_id, name, phone, email) -> bool:
        return False

    def delete_student(self, student_id) -> bool:
        return False

    def exists(self, student_id) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student WHERE student_id=?", (student_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def generate_student_id(self) -> str:
        return ""
