from abc import ABC, abstractmethod


class IScoreRepository(ABC):
    @abstractmethod
    def save_score(self, class_code, student_id, exam_type, score) -> None:
        pass

    @abstractmethod
    def get_scores_by_class_and_exam(self, class_code, exam_type) -> list:
        pass

    @abstractmethod
    def get_score(self, class_code, student_id, exam_type):
        pass
