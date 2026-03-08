"""Repository for Exam_Result and Exam_Result_Detailed table operations"""
from infrastructure.config.database import get_connection


class ExamResultRepository:
    """Manages Exam_Result and Exam_Result_Detailed records in SQL Server."""

    @staticmethod
    def get_next_exam_result_id() -> str:
        """Generate next exam_result_id like ER00001, ER00002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(exam_result_id, 3, LEN(exam_result_id)-2) AS INT)) FROM Exam_Result WHERE exam_result_id LIKE 'ER%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"ER{max_num + 1:05d}"

    @staticmethod
    def get_next_detail_id() -> str:
        """Generate next exam_result_detail_id like RD00001, RD00002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(exam_result_detail_id, 3, LEN(exam_result_detail_id)-2) AS INT)) FROM Exam_Result_Detailed WHERE exam_result_detail_id LIKE 'RD%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"RD{max_num + 1:05d}"

    # ==================== EXAM RESULT METHODS ====================

    @staticmethod
    def get_all_results() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT er.exam_result_id, er.exam_id, er.class_enrollment_id, 
                   er.overall_score, er.result_status,
                   e.exam_type, s.full_name
            FROM Exam_Result er
            LEFT JOIN Exam e ON er.exam_id = e.exam_id
            LEFT JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            LEFT JOIN Student s ON ce.student_id = s.student_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_result_by_id(exam_result_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT exam_result_id, exam_id, class_enrollment_id, overall_score, result_status 
            FROM Exam_Result WHERE exam_result_id=?
        """, (exam_result_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_results_by_exam(exam_id) -> list:
        """Get all results for an exam"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT er.exam_result_id, er.class_enrollment_id, s.full_name, 
                   er.overall_score, er.result_status
            FROM Exam_Result er
            LEFT JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            LEFT JOIN Student s ON ce.student_id = s.student_id
            WHERE er.exam_id=?
        """, (exam_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_results_by_student(student_id) -> list:
        """Get all exam results for a student"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT er.exam_result_id, e.exam_type, e.exam_date, c.class_name,
                   er.overall_score, er.result_status
            FROM Exam_Result er
            LEFT JOIN Exam e ON er.exam_id = e.exam_id
            LEFT JOIN Class c ON e.class_id = c.class_id
            LEFT JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            WHERE ce.student_id=?
        """, (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_result(data) -> str:
        """Insert exam result. data = (exam_result_id, exam_id, class_enrollment_id, overall_score, result_status). Returns exam_result_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exam_Result (exam_result_id, exam_id, class_enrollment_id, overall_score, result_status) 
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update_result(data) -> None:
        """Update exam result. data = (exam_result_id, overall_score, result_status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Exam_Result
            SET overall_score=?, result_status=?
            WHERE exam_result_id=?
        """, (data[1], data[2], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_result(exam_result_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Exam_Result WHERE exam_result_id=?", (exam_result_id,))
        conn.commit()
        conn.close()

    # ==================== EXAM RESULT DETAILED METHODS ====================

    @staticmethod
    def get_detailed_results(exam_result_id) -> list:
        """Get detailed skill scores for an exam result"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT erd.exam_result_detailed_id, erd.skill_id, sk.skill_name, erd.score
            FROM Exam_Result_Detailed erd
            LEFT JOIN Skill sk ON erd.skill_id = sk.skill_id
            WHERE erd.exam_result_id=?
        """, (exam_result_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_detailed_result(data) -> str:
        """Insert detailed result. data = (exam_result_detail_id, exam_result_id, skill_id, score). Returns exam_result_detail_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exam_Result_Detailed (exam_result_detail_id, exam_result_id, skill_id, score) 
            VALUES (?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update_detailed_result(data) -> None:
        """Update detailed result. data = (exam_result_detailed_id, score)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Exam_Result_Detailed SET score=? WHERE exam_result_detailed_id=?
        """, (data[1], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_detailed_result(exam_result_detailed_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Exam_Result_Detailed WHERE exam_result_detailed_id=?", (exam_result_detailed_id,))
        conn.commit()
        conn.close()
