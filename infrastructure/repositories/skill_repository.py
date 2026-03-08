"""Repository for Skill table operations"""
from infrastructure.config.database import get_connection


class SkillRepository:
    """Manages Skill records in SQL Server."""

    @staticmethod
    def get_next_skill_id() -> str:
        """Generate next skill_id like S01, S02, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(skill_id, 2, LEN(skill_id)-1) AS INT)) FROM Skill WHERE skill_id LIKE 'S%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"S{max_num + 1:02d}"

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.skill_id, s.course_id, s.skill_name, s.description, c.course_name
            FROM Skill s
            LEFT JOIN Course c ON s.course_id = c.course_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(skill_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT skill_id, course_id, skill_name, description FROM Skill WHERE skill_id=?",
            (skill_id,)
        )
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_by_course(course_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT skill_id, skill_name, description FROM Skill WHERE course_id=?",
            (course_id,)
        )
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> str:
        """Insert skill. data = (skill_id, course_id, skill_name, description). Returns skill_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Skill (skill_id, course_id, skill_name, description) 
            VALUES (?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update(data) -> None:
        """Update skill. data = (skill_id, course_id, skill_name, description)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Skill
            SET course_id=?, skill_name=?, description=?
            WHERE skill_id=?
        """, (data[1], data[2], data[3], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(skill_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Skill WHERE skill_id=?", (skill_id,))
        conn.commit()
        conn.close()
