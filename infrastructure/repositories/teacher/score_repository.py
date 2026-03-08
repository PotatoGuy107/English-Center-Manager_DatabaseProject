from domain.entities.score_entity import Score
from domain.interfaces.i_score_repository import IScoreRepository


class ScoreRepository(IScoreRepository):
    _scores = []

    def save_score(self, class_code, student_id, exam_type, score) -> None:
        for s in self._scores:
            if (
                s.class_code == class_code
                and s.student_id == student_id
                and s.exam_type == exam_type
            ):
                s.score = score
                return
        self._scores.append(Score(class_code, student_id, exam_type, score))

    def get_scores_by_class_and_exam(self, class_code, exam_type) -> list:
        return [
            s for s in self._scores
            if s.class_code == class_code and s.exam_type == exam_type
        ]

    def get_score(self, class_code, student_id, exam_type):
        for s in self._scores:
            if (
                s.class_code == class_code
                and s.student_id == student_id
                and s.exam_type == exam_type
            ):
                return s
        return None
