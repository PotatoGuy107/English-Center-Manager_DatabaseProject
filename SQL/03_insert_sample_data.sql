USE EnglishCenterDB;
GO

INSERT INTO Student (full_name, date_of_birth, gender, address, phone_number, email)
VALUES
(N'Nguyễn Văn An','2002-01-10',N'Male',N'HCM','0901111111','an@gmail.com'),
(N'Trần Thị Bình','2003-02-15',N'Female',N'HCM','0901111112','binh@gmail.com'),
(N'Lê Minh Châu','2001-03-12',N'Male',N'Hà Nội','0901111113','chau@gmail.com'),
(N'Phạm Thu Dung','2004-04-18',N'Female',N'HCM','0901111114','dung@gmail.com'),
(N'Hoàng Gia Huy','2000-05-21',N'Male',N'Đà Nẵng','0901111115','huy@gmail.com'),
(N'Đặng Thị Lan','2003-06-11',N'Female',N'HCM','0901111116','lan@gmail.com'),
(N'Ngô Văn Minh','2002-07-09',N'Male',N'Hà Nội','0901111117','minh@gmail.com'),
(N'Bùi Khánh Ngọc','2005-08-14',N'Female',N'HCM','0901111118','ngoc@gmail.com'),
(N'Phan Quốc Phong','2001-09-22',N'Male',N'HCM','0901111119','phong@gmail.com'),
(N'Võ Thị Quỳnh','2003-10-30',N'Female',N'HCM','0901111120','quynh@gmail.com');

INSERT INTO Course (course_name, description, level, duration_weeks, tuition_fee)
VALUES
(N'IELTS Foundation',N'Basic IELTS',N'Beginner',12,3500000),
(N'IELTS Intermediate',N'IELTS mid',N'Intermediate',16,4500000),
(N'IELTS Advanced',N'IELTS high',N'Advanced',20,5500000),
(N'English Basic',N'Basic English',N'Beginner',10,3000000),
(N'English Communication',N'Speaking focus',N'Intermediate',12,3200000),
(N'Grammar Master',N'Grammar course',N'Intermediate',10,2800000),
(N'TOEIC 500+',N'TOEIC basic',N'Beginner',12,3300000),
(N'TOEIC 750+',N'TOEIC mid',N'Intermediate',16,4200000),
(N'TOEFL Intro',N'TOEFL basic',N'Intermediate',14,4600000),
(N'Business English',N'Workplace English',N'Advanced',12,5000000);

INSERT INTO Enrollment (student_id, course_id, start_date, end_date, enrollment_status)
VALUES
(1,1,'2025-01-01','2025-03-30','studying'),
(2,1,'2025-01-01','2025-03-30','studying'),
(3,2,'2025-02-01','2025-05-30','pending'),
(4,3,'2025-01-15','2025-05-15','studying'),
(5,4,'2025-03-01','2025-05-01','completed'),
(6,5,'2025-02-01','2025-04-30','studying'),
(7,6,'2025-02-01','2025-04-01','cancelled'),
(8,7,'2025-01-01','2025-03-01','studying'),
(9,8,'2025-02-01','2025-05-01','pending'),
(10,9,'2025-02-01','2025-05-01','studying');

INSERT INTO Payment (enrollment_id, amount, payment_status, note)
VALUES
(1,3500000,'paid',N'Full'),
(2,2000000,'partial',N'First'),
(3,0,'unpaid',N''),
(4,5500000,'paid',N'Full'),
(5,3000000,'paid',N'Full'),
(6,1500000,'partial',N'First'),
(7,0,'unpaid',N''),
(8,3300000,'paid',N'Full'),
(9,0,'unpaid',N''),
(10,4600000,'paid',N'Full');

INSERT INTO Skill (course_id, skill_name, description)
VALUES
(1,N'Listening',N'IELTS Listening'),
(1,N'Reading',N'IELTS Reading'),
(2,N'Speaking',N'IELTS Speaking'),
(2,N'Writing',N'IELTS Writing'),
(3,N'Advanced Writing',N''),
(4,N'Basic Speaking',N''),
(5,N'Conversation',N''),
(6,N'Grammar',N''),
(7,N'TOEIC Listening',N''),
(8,N'TOEIC Reading',N'');

INSERT INTO Teacher (full_name, phone_number, email, specialization, hire_date)
VALUES
(N'John Smith','0911111111','john@center.com',N'IELTS','2023-01-01'),
(N'Mary Jane','0911111112','mary@center.com',N'Speaking','2023-02-01'),
(N'David Lee','0911111113','david@center.com',N'Grammar','2023-03-01'),
(N'Anna Kim','0911111114','anna@center.com',N'Writing','2023-04-01'),
(N'Chris Wong','0911111115','chris@center.com',N'Listening','2023-05-01'),
(N'Sarah Brown','0911111116','sarah@center.com',N'Reading','2023-06-01'),
(N'Linda Park','0911111117','linda@center.com',N'TOEIC','2023-07-01'),
(N'James Tran','0911111118','james@center.com',N'IELTS','2023-08-01'),
(N'Mike Nguyen','0911111119','mike@center.com',N'Communication','2023-09-01'),
(N'Lisa Ho','0911111120','lisa@center.com',N'Business','2023-10-01');

INSERT INTO Class (skill_id, teacher_id, class_name, start_date, end_date, max_student, status)
VALUES
(1,1,N'Listening A','2025-01-01','2025-02-15',20,'ongoing'),
(2,2,N'Reading A','2025-01-01','2025-02-15',20,'planned'),
(3,3,N'Speaking B','2025-01-01','2025-02-15',20,'ongoing'),
(4,4,N'Writing B','2025-01-01','2025-02-15',20,'completed'),
(5,5,N'Writing C','2025-02-01','2025-03-15',20,'planned'),
(6,6,N'Speaking Basic','2025-02-01','2025-03-15',20,'ongoing'),
(7,7,N'Conversation','2025-02-01','2025-03-15',20,'planned'),
(8,8,N'Grammar A','2025-02-01','2025-03-15',20,'completed'),
(9,9,N'TOEIC Listening','2025-02-01','2025-03-15',20,'ongoing'),
(10,10,N'TOEIC Reading','2025-02-01','2025-03-15',20,'planned');

INSERT INTO Class_Enrollment (student_id, class_id)
VALUES
(1,1),(2,1),(3,2),(4,3),(5,4),
(6,5),(7,6),(8,7),(9,8),(10,9);

INSERT INTO Exam (class_id, exam_type, exam_date)
VALUES
(1,N'Midterm','2025-01-20'),
(1,N'Final','2025-02-15'),
(3,N'Midterm','2025-01-25'),
(3,N'Final','2025-02-15'),
(4,N'Final','2025-02-15'),
(6,N'Midterm','2025-02-10'),
(6,N'Final','2025-03-15'),
(9,N'Midterm','2025-02-10'),
(9,N'Final','2025-03-15'),
(2,N'Midterm','2025-01-25');

INSERT INTO Exam_Result (exam_id, class_enrollment_id, overall_score, result_status)
VALUES
(1,1,7.5,'pass'),
(2,2,6.0,'pass'),
(3,3,5.5,'fail'),
(4,4,8.0,'pass'),
(5,5,7.0,'pass'),
(6,6,6.5,'pass'),
(7,7,5.0,'fail'),
(8,8,7.8,'pass'),
(9,9,6.9,'pass'),
(10,10,5.5,'fail');

INSERT INTO Exam_Result_Detailed (exam_result_id, skill_id, score)
VALUES
(1,1,8),(2,1,6),(3,3,5),(4,4,8),(5,5,7),
(6,6,6),(7,7,5),(8,8,7),(9,9,6),(10,10,5);

INSERT INTO Room (room_name, capacity, location)
VALUES
(N'Room A',25,N'Floor 1'),
(N'Room B',25,N'Floor 1'),
(N'Room C',30,N'Floor 2'),
(N'Room D',30,N'Floor 2'),
(N'Room E',20,N'Floor 1'),
(N'Room F',20,N'Floor 2'),
(N'Room G',25,N'Floor 3'),
(N'Room H',25,N'Floor 3'),
(N'Room I',30,N'Floor 4'),
(N'Room J',30,N'Floor 4');

INSERT INTO Schedule (class_id, room_id, study_date, time_slot, start_time, end_time)
VALUES
(1,1,'2025-01-05',N'Morning','08:00','10:00'),
(1,1,'2025-01-07',N'Morning','08:00','10:00'),
(2,2,'2025-01-05',N'Afternoon','13:00','15:00'),
(3,3,'2025-01-06',N'Morning','08:00','10:00'),
(4,4,'2025-01-06',N'Afternoon','13:00','15:00'),
(5,5,'2025-02-05',N'Morning','08:00','10:00'),
(6,6,'2025-02-05',N'Afternoon','13:00','15:00'),
(7,7,'2025-02-06',N'Morning','08:00','10:00'),
(8,8,'2025-02-06',N'Afternoon','13:00','15:00'),
(9,9,'2025-02-07',N'Morning','08:00','10:00');