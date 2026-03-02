from DAL.teacher.score_dal import ScoreDAL
from DAL.dshv_dal import FakeStudentRepository


class nhapdiemBLL:
    def __init__(self):
        self.score_dal = ScoreDAL()
        self.student_repo = FakeStudentRepository()

    def get_students_by_class(self, class_code):
        return self.student_repo.get_students_by_class(class_code)

    def save_score(self, class_code, student_id, ky_thi, diem):
        self.score_dal.save_score(class_code, student_id, ky_thi, diem)

    def get_scores(self, class_code, ky_thi):
        return self.score_dal.get_scores_by_class_and_exam(class_code, ky_thi)
