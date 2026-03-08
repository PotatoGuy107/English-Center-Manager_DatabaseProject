from domain.entities.score_entity import Score
from domain.interfaces.i_score_repository import IScoreRepository
from infrastructure.config.database import get_connection


class ScoreRepository(IScoreRepository):

    def save_score(self, class_code, student_id, exam_type, score) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if score exists
        cursor.execute("""
            SELECT score_id FROM Score 
            WHERE class_id=? AND student_id=? AND exam_id=?
        """, (class_code, student_id, exam_type))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing score
            cursor.execute("""
                UPDATE Score SET score=? 
                WHERE class_id=? AND student_id=? AND exam_id=?
            """, (score, class_code, student_id, exam_type))
        else:
            # Generate new score_id
            cursor.execute("SELECT TOP 1 score_id FROM Score ORDER BY score_id DESC")
            row = cursor.fetchone()
            if row:
                num = int(row[0].replace("SC", "")) + 1
                score_id = f"SC{num:03d}"
            else:
                score_id = "SC001"
            
            # Insert new score
            cursor.execute("""
                INSERT INTO Score (score_id, student_id, class_id, exam_id, score)
                VALUES (?, ?, ?, ?, ?)
            """, (score_id, student_id, class_code, exam_type, score))
        
        conn.commit()
        conn.close()

    def get_scores_by_class_and_exam(self, class_code, exam_type) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT class_id, student_id, exam_id, score FROM Score
            WHERE class_id=? AND exam_id=?
        """, (class_code, exam_type))
        rows = cursor.fetchall()
        conn.close()
        
        return [Score(r[0], r[1], r[2], r[3]) for r in rows]

    def get_score(self, class_code, student_id, exam_type):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT class_id, student_id, exam_id, score FROM Score
            WHERE class_id=? AND student_id=? AND exam_id=?
        """, (class_code, student_id, exam_type))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Score(row[0], row[1], row[2], row[3])
        return None
