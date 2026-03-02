from MODELS.ScoreModel import Score


class ScoreDAL:
    _scores = []
    def __init__(self):
        pass

    def save_score(self, class_code, student_id, ky_thi, diem):

        # Kiểm tra đã tồn tại chưa
        for score in self._scores:
            if (score.class_code == class_code and
                score.student_id == student_id and
                score.ky_thi == ky_thi):

                # Nếu tồn tại → update
                score.diem = diem
                return

        # Nếu chưa tồn tại → thêm mới
        new_score = Score(class_code, student_id, ky_thi, diem)
        self._scores.append(new_score)

    def get_scores_by_class_and_exam(self, class_code, ky_thi):
        return [
            s for s in self._scores
            if s.class_code == class_code and s.ky_thi == ky_thi
        ]


    # LẤY 1 ĐIỂM CỤ THỂ

    def get_score(self, class_code, student_id, ky_thi):
        for s in self._scores:
            if (s.class_code == class_code and
                s.student_id == student_id and
                s.ky_thi == ky_thi):
                return s

        return None