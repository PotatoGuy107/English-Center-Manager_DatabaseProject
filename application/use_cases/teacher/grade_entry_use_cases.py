from infrastructure.repositories.teacher.score_repository import ScoreRepository
from infrastructure.repositories.student_repository import StudentRepository


class GradeEntryUseCases:
    def __init__(self):
        self.score_repo = ScoreRepository()
        self.student_repo = StudentRepository()

    def get_students_by_class(self, class_code) -> list:
        return self.student_repo.get_students_by_class(class_code)

    def save_score(self, class_code, student_id, exam_type, score) -> None:
        self.score_repo.save_score(class_code, student_id, exam_type, score)

    def get_scores(self, class_code, exam_type) -> list:
        return self.score_repo.get_scores_by_class_and_exam(class_code, exam_type)
