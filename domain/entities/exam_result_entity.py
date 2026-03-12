class ExamResult:
    """ExamResult entity matching SQL Server Exam_Result table"""
    def __init__(
        self,
        exam_result_id: int = None,
        exam_id: int = None,
        class_enrollment_id: int = None,
        overall_score: float = None,
        result_status: str = None,
    ):
        self.exam_result_id = exam_result_id
        self.exam_id = exam_id
        self.class_enrollment_id = class_enrollment_id
        self.overall_score = overall_score
        self.result_status = result_status


class ExamResultDetailed:
    """ExamResultDetailed entity matching SQL Server Exam_Result_Detailed table"""
    def __init__(
        self,
        exam_result_detailed_id: int = None,
        exam_result_id: int = None,
        skill_id: int = None,
        score: float = None,
    ):
        self.exam_result_detailed_id = exam_result_detailed_id
        self.exam_result_id = exam_result_id
        self.skill_id = skill_id
        self.score = score
