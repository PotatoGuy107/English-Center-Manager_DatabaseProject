-- Enrollment
CREATE INDEX IX_Enrollment_StudentId ON Enrollment(student_id);
CREATE INDEX IX_Enrollment_CourseId ON Enrollment(course_id);

-- Payment
CREATE INDEX IX_Payment_EnrollmentId ON Payment(enrollment_id);

-- Skill
CREATE INDEX IX_Skill_CourseId ON Skill(course_id);

-- Class
CREATE INDEX IX_Class_SkillId ON Class(skill_id);
CREATE INDEX IX_Class_TeacherId ON Class(teacher_id);

-- Class_Enrollment
CREATE INDEX IX_ClassEnrollment_StudentId ON Class_Enrollment(student_id);
CREATE INDEX IX_ClassEnrollment_ClassId ON Class_Enrollment(class_id);
CREATE UNIQUE INDEX IX_ClassEnrollment_Student_Class 
ON Class_Enrollment(student_id, class_id);

-- Exam
CREATE INDEX IX_Exam_ClassId ON Exam(class_id);
CREATE INDEX IX_Exam_ExamDate ON Exam(exam_date);

-- Exam_Result
CREATE INDEX IX_ExamResult_ExamId ON Exam_Result(exam_id);
CREATE INDEX IX_ExamResult_ClassEnrollmentId ON Exam_Result(class_enrollment_id);

-- Exam_Result_Detailed
CREATE INDEX IX_ExamResultDetail_ResultId ON Exam_Result_Detailed(exam_result_id);
CREATE INDEX IX_ExamResultDetail_SkillId ON Exam_Result_Detailed(skill_id);

-- Schedule
CREATE INDEX IX_Schedule_ClassId ON Schedule(class_id);
CREATE INDEX IX_Schedule_Room_Date ON Schedule(room_id, study_date);