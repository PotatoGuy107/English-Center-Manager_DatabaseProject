from domain.entities.score_entity import Score
from domain.interfaces.i_score_repository import IScoreRepository
from infrastructure.config.database import get_connection


class ScoreRepository(IScoreRepository):
    """Repository for scores using Exam_Result and Exam_Result_Detailed tables in SQL Server."""

    def save_score(self, class_code, student_id, exam_type, score) -> None:
        """Save/update overall score for a student in an exam.
        Finds the exam by class_id and exam_type, then updates Exam_Result.
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Find the exam_result for this student+exam
        cursor.execute("""
            SELECT er.exam_result_id
            FROM Exam_Result er
            INNER JOIN Exam e ON er.exam_id = e.exam_id
            INNER JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            WHERE e.class_id = ? AND ce.student_id = ? AND e.exam_type = ?
        """, (class_code, student_id, exam_type))
        row = cursor.fetchone()

        if row:
            # Update existing exam result
            cursor.execute("""
                UPDATE Exam_Result SET overall_score = ?,
                    result_status = CASE WHEN ? >= 5.0 THEN 'pass' ELSE 'fail' END
                WHERE exam_result_id = ?
            """, (score, score, row[0]))
        else:
            # Find the exam
            cursor.execute("""
                SELECT e.exam_id FROM Exam e WHERE e.class_id = ? AND e.exam_type = ?
            """, (class_code, exam_type))
            exam_row = cursor.fetchone()
            if not exam_row:
                conn.close()
                return

            # Find class_enrollment
            cursor.execute("""
                SELECT ce.class_enrollment_id FROM Class_Enrollment ce
                WHERE ce.class_id = ? AND ce.student_id = ?
            """, (class_code, student_id))
            ce_row = cursor.fetchone()
            if not ce_row:
                conn.close()
                return

            # Insert new exam result
            cursor.execute("""
                INSERT INTO Exam_Result (exam_id, class_enrollment_id, overall_score, result_status)
                VALUES (?, ?, ?, ?)
            """, (exam_row[0], ce_row[0], score, 'pass' if score >= 5.0 else 'fail'))

        conn.commit()
        conn.close()

    def get_scores_by_class_and_exam(self, class_code, exam_type) -> list:
        """Get all scores for a class + exam type."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.student_id, er.overall_score
            FROM Exam_Result er
            INNER JOIN Exam e ON er.exam_id = e.exam_id
            INNER JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            WHERE e.class_id = ? AND e.exam_type = ?
        """, (class_code, exam_type))
        rows = cursor.fetchall()
        conn.close()

        return [Score(class_code, r[0], exam_type, r[1]) for r in rows]

    def get_score(self, class_code, student_id, exam_type):
        """Get single score for a student in a specific exam."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.student_id, er.overall_score
            FROM Exam_Result er
            INNER JOIN Exam e ON er.exam_id = e.exam_id
            INNER JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
            WHERE e.class_id = ? AND ce.student_id = ? AND e.exam_type = ?
        """, (class_code, student_id, exam_type))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Score(class_code, row[0], exam_type, row[1])
        return None
