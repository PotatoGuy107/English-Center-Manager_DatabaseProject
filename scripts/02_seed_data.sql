USE EnglishCenterDB;


DECLARE @i INT = 1;

WHILE @i <= 200
BEGIN
    INSERT INTO Student (
        student_id,
        full_name,
        date_of_birth,
        gender,
        address,
        phone_number,
        email,
        register_date,
        status
    )
    VALUES (
        CONCAT('ST', RIGHT('000' + CAST(@i AS VARCHAR), 3)),
        CONCAT(N'Học viên ', @i),
        DATEADD(YEAR, -18 - (@i % 5), GETDATE()),
        CASE WHEN @i % 2 = 0 THEN 'Female' ELSE 'Male' END,
        N'Hồ Chí Minh',
        CONCAT('09', RIGHT('00000000' + CAST(@i AS VARCHAR), 8)),
        CONCAT('student', @i, '@mail.com'),
        GETDATE(),
        'Active'
    );

    SET @i += 1;
END;


INSERT INTO Course VALUES
('C01', N'English Communication Basic', N'Tiếng Anh giao tiếp cơ bản', 'Basic', 10, 3000000, 'Active'),
('C02', N'English Starter', N'Lớp nền tảng cho người mới bắt đầu', 'Starter', 8, 2500000, 'Active'),
('C03', N'Cambridge Mover', N'Lớp luyện thi Cambridge Mover', 'Mover', 12, 3500000, 'Active'),
('C04', N'Cambridge Flyer', N'Lớp luyện thi Cambridge Flyer', 'Flyer', 14, 4000000, 'Active'),
('C05', N'IELTS 5.0', N'Lớp luyện IELTS mục tiêu 5.0', 'IELTS', 12, 6000000, 'Active'),
('C06', N'IELTS 6.0', N'Lớp luyện IELTS mục tiêu 6.0', 'IELTS', 14, 8000000, 'Active');

INSERT INTO Skill VALUES
-- English Communication Basic
('S01', 'C01', 'Communication Listening',  N'Listening skills for Communication'),
('S02', 'C01', 'Communication Speaking',   N'Speaking skills for Communication'),

-- Starter
('S03', 'C02', 'Basic Listening',  N'Basic Listening for beginners'),
('S04', 'C02', 'Basic Speaking',   N'Basic Speaking for beginners'),
('S05', 'C02', 'Basic Reading',    N'Basic Reading for beginners'),
('S06', 'C02', 'Basic Writing',    N'Basic Writing for beginners'),

-- Cambridge Mover
('S07', 'C03', 'Listening',  N'Listening skills for Cambridge Mover'),
('S08', 'C03', 'Speaking',   N'Speaking skills for Cambridge Mover'),
('S09', 'C03', 'Reading',    N'Reading skills for Cambridge Mover'),
('S10', 'C03', 'Writing',    N'Writing skills for Cambridge Mover'),

-- Cambridge Flyer
('S11', 'C04', 'Listening',  N'Listening skills for Cambridge Flyer'),
('S12', 'C04', 'Speaking',   N'Speaking skills for Cambridge Flyer'),
('S13', 'C04', 'Reading',    N'Reading skills for Cambridge Flyer'),
('S14', 'C04', 'Writing',    N'Writing skills for Cambridge Flyer'),

-- IELTS 5.0
('S15', 'C05', 'Listening',  N'Listening skills for IELTS 5.0'),
('S16', 'C05', 'Speaking',   N'Speaking skills for IELTS 5.0'),
('S17', 'C05', 'Reading',    N'Reading skills for IELTS 5.0'),
('S18', 'C05', 'Writing',    N'Writing skills for IELTS 5.0'),

-- IELTS 6.0
('S19', 'C06', 'Listening',  N'Listening skills for IELTS 6.0'),
('S20', 'C06', 'Speaking',   N'Speaking skills for IELTS 6.0'),
('S21', 'C06', 'Reading',    N'Reading skills for IELTS 6.0'),
('S22', 'C06', 'Writing',    N'Writing skills for IELTS 6.0');


INSERT INTO Teacher (teacher_id, full_name, phone_number, email, specialization, hire_date, status)
VALUES
('T01',N'Nguyễn Minh Anh','0901111111','anh.nguyen@center.com',N'Giao tiếp',GETDATE(),'Active'),
('T02',N'Trần Thu Hà','0902222222','ha.tran@center.com',N'Starter',GETDATE(),'Active'),
('T03',N'Lê Hoàng Nam','0903333333','nam.le@center.com',N'Mover',GETDATE(),'Active'),
('T04',N'Phạm Quỳnh Chi','0904444444','chi.pham@center.com',N'Flyer',GETDATE(),'Active'),
('T05',N'Đỗ Thành Công','0905555555','cong.do@center.com',N'IELTS 5.0',GETDATE(),'Active'),
('T06',N'Võ Mỹ Linh','0906666666','linh.vo@center.com',N'IELTS 6.0',GETDATE(),'Active'),
('T07',N'Bùi Quốc Bảo','0907777777','bao.bui@center.com',N'Reading/Writing',GETDATE(),'Active'),
('T08',N'Hoàng Gia Hân','0908888888','han.hoang@center.com',N'Listening/Speaking',GETDATE(),'Active');


INSERT INTO Room (room_id, room_name, capacity, location, status)
VALUES
('R01',N'Phòng 101',25,N'Tầng 1','Available'),
('R02',N'Phòng 102',25,N'Tầng 1','Available'),
('R03',N'Phòng 201',30,N'Tầng 2','Available'),
('R04',N'Phòng 202',30,N'Tầng 2','Available'),
('R05',N'Phòng Lab 1',20,N'Tầng 3','Available'),
('R06',N'Phòng Lab 2',20,N'Tầng 3','Available');


INSERT INTO Class
(class_id, class_name, skill_id, teacher_id, start_date, end_date, max_student, status)
SELECT
    CONCAT('CL', RIGHT('00' + CAST(ROW_NUMBER() OVER(ORDER BY skill_id) AS VARCHAR),2)),
    CONCAT(N'Lớp ', skill_name, ' ', skill_id),
    skill_id,
    (SELECT TOP 1 teacher_id FROM Teacher ORDER BY NEWID()),
    GETDATE(),
    DATEADD(MONTH,3,GETDATE()),
    25,
    'Active'
FROM Skill;



WITH ClassCTE AS (
    SELECT 
        class_id,
        ROW_NUMBER() OVER (ORDER BY class_id) AS rn
    FROM Class
)

INSERT INTO Schedule
(schedule_id, class_id, room_id, study_date, time_slot, start_time, end_time)
SELECT
    CONCAT('SC', RIGHT('000' + CAST(ROW_NUMBER() OVER(ORDER BY c.class_id, v.day_offset) AS VARCHAR),3)),
    c.class_id,
    (SELECT TOP 1 room_id FROM Room ORDER BY NEWID()),
    DATEADD(DAY, v.day_offset, GETDATE()),
    
    CASE (c.rn % 3)
        WHEN 1 THEN 'Ca 1'
        WHEN 2 THEN 'Ca 2'
        ELSE 'Ca 3'
    END,

    CASE (c.rn % 3)
        WHEN 1 THEN '07:00'
        WHEN 2 THEN '13:00'
        ELSE '18:00'
    END,

    CASE (c.rn % 3)
        WHEN 1 THEN '10:00'
        WHEN 2 THEN '16:00'
        ELSE '21:00'
    END
FROM ClassCTE c
CROSS JOIN (VALUES (1),(3)) v(day_offset);  -- 2 buổi cách nhau 2 ngày



INSERT INTO Enrollment
(enrollment_id, student_id, course_id, enrollment_date, start_date, end_date, enrollment_status)
SELECT
    CONCAT('EN', RIGHT('000' + CAST(ROW_NUMBER() OVER(ORDER BY student_id) AS VARCHAR),3)),
    student_id,
    CASE 
        WHEN ROW_NUMBER() OVER(ORDER BY student_id) <= 40 THEN 'C01'
        WHEN ROW_NUMBER() OVER(ORDER BY student_id) <= 80 THEN 'C02'
        WHEN ROW_NUMBER() OVER(ORDER BY student_id) <= 120 THEN 'C03'
        WHEN ROW_NUMBER() OVER(ORDER BY student_id) <= 150 THEN 'C04'
        WHEN ROW_NUMBER() OVER(ORDER BY student_id) <= 175 THEN 'C05'
        ELSE 'C06'
    END,
    GETDATE(),
    GETDATE(),
    DATEADD(MONTH,3,GETDATE()),
    'Active'
FROM Student;



INSERT INTO Class_Enrollment
(class_enrollment_id, student_id, class_id, join_date, status)
SELECT
    CONCAT('CE', RIGHT('000' + CAST(ROW_NUMBER() OVER(ORDER BY e.student_id) AS VARCHAR),3)),
    e.student_id,
    c.class_id,
    GETDATE(),
    'Studying'
FROM Enrollment e
JOIN Skill s ON e.course_id = s.course_id
JOIN Class c ON c.skill_id = s.skill_id
WHERE c.class_id IN (
    SELECT TOP 1 class_id 
    FROM Class c2 
    JOIN Skill s2 ON c2.skill_id = s2.skill_id
    WHERE s2.course_id = e.course_id
);



WITH ClassCTE AS (
    SELECT 
        class_id,
        ROW_NUMBER() OVER (ORDER BY class_id) AS rn
    FROM Class
)

INSERT INTO Exam
(exam_id, class_id, exam_type, exam_date, description)
SELECT
    CONCAT('EX', RIGHT('000' + CAST((rn*2 - 1) AS VARCHAR),3)),
    class_id,
    'Midterm',
    DATEADD(MONTH,2,GETDATE()),
    N'Kiểm tra giữa kỳ'
FROM ClassCTE

UNION ALL

SELECT
    CONCAT('EX', RIGHT('000' + CAST((rn*2) AS VARCHAR),3)),
    class_id,
    'Final',
    DATEADD(MONTH,3,GETDATE()),
    N'Kiểm tra cuối kỳ'
FROM ClassCTE;



INSERT INTO Payment
(payment_id, enrollment_id, amount, payment_date, payment_status,note)
SELECT
    CONCAT('PM', RIGHT('000' + CAST(ROW_NUMBER() OVER(ORDER BY enrollment_id) AS VARCHAR),3)),
    enrollment_id,
    3000000,
    GETDATE(),
    'Paid',
    'Cash'
FROM Enrollment;


INSERT INTO Exam_Result
(exam_result_id, exam_id, class_enrollment_id, overall_score, result_status)
SELECT
    CONCAT('ER', RIGHT('00000' + 
        CAST(ROW_NUMBER() OVER(ORDER BY e.exam_id, ce.class_enrollment_id) AS VARCHAR),5)),
    e.exam_id,
    ce.class_enrollment_id,
    NULL,
    NULL
FROM Exam e
JOIN Class_Enrollment ce 
    ON e.class_id = ce.class_id;



INSERT INTO Exam_Result_Detailed
(exam_result_detail_id, exam_result_id, skill_id, score)
SELECT
    CONCAT('RD', RIGHT('00000' + 
        CAST(ROW_NUMBER() OVER(ORDER BY er.exam_result_id, s.skill_id) AS VARCHAR),5)),
    er.exam_result_id,
    s.skill_id,

    CASE 
        -- IELTS
        WHEN s.course_id = 'C05' 
            THEN CAST(ROUND(RAND(CHECKSUM(NEWID())) * 2 + 4,1) AS DECIMAL(3,1)) -- 4.0–6.0
        WHEN s.course_id = 'C06'
            THEN CAST(ROUND(RAND(CHECKSUM(NEWID())) * 2 + 5,1) AS DECIMAL(3,1)) -- 5.0–7.0

        -- Cambridge (shield 1–5)
        WHEN s.course_id IN ('C02','C03','C04')
            THEN CAST(ROUND(RAND(CHECKSUM(NEWID())) * 4 + 1,0) AS INT)

        -- Giao tiếp
        ELSE CAST(ROUND(RAND(CHECKSUM(NEWID())) * 4 + 6,1) AS DECIMAL(3,1))
    END

FROM Exam_Result er
JOIN Exam e ON er.exam_id = e.exam_id
JOIN Class c ON e.class_id = c.class_id
JOIN Skill sk ON c.skill_id = sk.skill_id
JOIN Skill s ON s.course_id = sk.course_id;

UPDATE er
SET overall_score =
    CASE 
        -- Cambridge → SUM shield
        WHEN s.course_id IN ('C02','C03','C04')
            THEN sub.total_score

        -- IELTS & Giao tiếp → AVG
        ELSE sub.avg_score
    END
FROM Exam_Result er
JOIN (
    SELECT 
        exam_result_id,
        SUM(score) AS total_score,
        CAST(AVG(CAST(score AS FLOAT)) AS DECIMAL(3,1)) AS avg_score
    FROM Exam_Result_Detailed
    GROUP BY exam_result_id
) sub
ON er.exam_result_id = sub.exam_result_id
JOIN Exam e ON er.exam_id = e.exam_id
JOIN Class c ON e.class_id = c.class_id
JOIN Skill sk ON c.skill_id = sk.skill_id
JOIN Skill s ON sk.course_id = s.course_id;

UPDATE er
SET result_status =
    CASE 
        WHEN s.course_id = 'C05' AND er.overall_score >= 5.0 THEN 'Pass'
        WHEN s.course_id = 'C06' AND er.overall_score >= 6.0 THEN 'Pass'
        WHEN s.course_id IN ('C02','C03','C04') AND er.overall_score >= 10 THEN 'Pass'
        WHEN s.course_id = 'C01' AND er.overall_score >= 5.0 THEN 'Pass'
        ELSE 'Fail'
    END
FROM Exam_Result er
JOIN Exam e ON er.exam_id = e.exam_id
JOIN Class c ON e.class_id = c.class_id
JOIN Skill sk ON c.skill_id = sk.skill_id
JOIN Skill s ON sk.course_id = s.course_id;

