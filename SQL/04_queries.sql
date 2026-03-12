Câu 1 — Danh sách học viên học khóa IELTS

Truy vấn sử dụng phép nối giữa bảng Student, Enrollment và Course nhằm xác định các học viên đang tham gia các khóa học liên quan đến IELTS. Điều kiện LIKE được dùng để lọc linh hoạt theo tên khóa học, và kết quả được sắp xếp theo tên học viên để dễ tra cứu.

SELECT s.student_id, s.full_name, s.email, 
       c.course_name, e.enrollment_status
FROM Student s
JOIN Enrollment e ON s.student_id = e.student_id
JOIN Course c ON e.course_id = c.course_id
WHERE c.course_name LIKE N'%IELTS%'
ORDER BY s.full_name;
Câu 2 — Khóa học có nhiều học viên

Truy vấn thực hiện thống kê số lượng học viên theo từng khóa học bằng GROUP BY và lọc bằng HAVING để chỉ hiển thị các khóa có hơn 2 học viên.

SELECT c.course_name, COUNT(e.student_id) AS so_hoc_vien
FROM Course c
JOIN Enrollment e ON c.course_id = e.course_id
GROUP BY c.course_name
HAVING COUNT(e.student_id) > 2
ORDER BY so_hoc_vien DESC;
Câu 3 — Giảng viên dạy lớp Planned

Truy vấn sử dụng subquery để xác định các giảng viên đang phụ trách ít nhất một lớp có trạng thái Planned.

SELECT teacher_id, full_name, specialization, email
FROM Teacher
WHERE teacher_id IN (
    SELECT DISTINCT teacher_id
    FROM Class
    WHERE status = 'Planned'
);
Câu 4 — Học viên chưa thanh toán

Truy vấn sử dụng EXISTS để tìm các học viên có đăng ký nhưng chưa hoàn tất thanh toán.

SELECT s.student_id, s.full_name, s.phone_number
FROM Student s
WHERE EXISTS (
    SELECT 1
    FROM Enrollment e
    WHERE e.student_id = s.student_id
      AND NOT EXISTS (
          SELECT 1
          FROM Payment p
          WHERE p.enrollment_id = e.enrollment_id
            AND p.payment_status = 'paid'
      )
);
Câu 5 — Phân loại theo độ tuổi

Truy vấn dùng CASE WHEN để phân loại học viên theo nhóm tuổi dựa trên ngày sinh.

SELECT student_id, full_name, date_of_birth,
    CASE
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) < 12 THEN N'Thiếu nhi'
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) BETWEEN 12 AND 15 THEN N'Thiếu niên'
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) BETWEEN 16 AND 22 THEN N'Thanh niên'
        ELSE N'Trưởng thành'
    END AS nhom_tuoi
FROM Student
ORDER BY date_of_birth;
Câu 6 — Xếp hạng học viên trong lớp

Truy vấn sử dụng ROW_NUMBER để xếp hạng học viên theo điểm tổng kết trong từng lớp.

SELECT c.class_name, s.full_name, er.overall_score,
       ROW_NUMBER() OVER (
           PARTITION BY e.class_id
           ORDER BY er.overall_score DESC
       ) AS xep_hang_trong_lop
FROM Exam_Result er
JOIN Exam e ON er.exam_id = e.exam_id
JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
JOIN Student s ON ce.student_id = s.student_id
JOIN Class c ON e.class_id = c.class_id
WHERE er.overall_score IS NOT NULL;
Câu 7 — Doanh thu theo khóa học

CTE được dùng để tính tổng doanh thu theo khóa học và lọc các khóa có doanh thu cao.

WITH DoanhThuKhoa AS (
    SELECT c.course_id, c.course_name,
           SUM(p.amount) AS tong_doanh_thu,
           COUNT(DISTINCT e.student_id) AS so_hoc_vien
    FROM Course c
    JOIN Enrollment e ON c.course_id = e.course_id
    JOIN Payment p ON e.enrollment_id = p.enrollment_id
    GROUP BY c.course_id, c.course_name
)
SELECT course_name, tong_doanh_thu, so_hoc_vien
FROM DoanhThuKhoa
WHERE tong_doanh_thu > 10000000
ORDER BY tong_doanh_thu DESC;
Câu 8 — Danh bạ liên hệ chung

Truy vấn sử dụng UNION để kết hợp danh sách học viên và giảng viên thành một danh bạ chung.

SELECT full_name, phone_number, email, N'Học viên' AS vai_tro
FROM Student
WHERE email LIKE '%gmail%'

UNION

SELECT full_name, phone_number, email, N'Giảng viên'
FROM Teacher
WHERE email LIKE '%center%'

ORDER BY vai_tro, full_name;
Câu 9 — Phòng học sử dụng theo thời gian

Truy vấn xác định các phòng học đã được sử dụng trong một khoảng thời gian cụ thể.

SELECT DISTINCT r.room_id, r.room_name, r.capacity, r.location
FROM Room r
JOIN Schedule sc ON r.room_id = sc.room_id
WHERE sc.study_date BETWEEN '2024-01-01' AND '2024-06-30'
ORDER BY r.room_name;
Câu 10 — Top giảng viên dạy nhiều lớp

Truy vấn xác định top 5 giảng viên có khối lượng giảng dạy lớn nhất.

SELECT TOP 5 
    t.teacher_id, t.full_name, t.specialization,
    COUNT(DISTINCT c.class_id) AS so_lop_day,
    COUNT(DISTINCT ce.student_id) AS tong_hoc_vien
FROM Teacher t
JOIN Class c ON t.teacher_id = c.teacher_id
LEFT JOIN Class_Enrollment ce ON c.class_id = ce.class_id
GROUP BY t.teacher_id, t.full_name, t.specialization
ORDER BY so_lop_day DESC, tong_hoc_vien DESC;
Câu 11 — Tỷ lệ lấp đầy lớp

Truy vấn tính tỷ lệ lấp đầy và phân loại tình trạng lớp.

SELECT c.class_id, c.class_name, c.max_student,
       (SELECT COUNT(*) FROM Class_Enrollment ce WHERE ce.class_id = c.class_id) AS si_so,
       CAST(
           (SELECT COUNT(*) FROM Class_Enrollment ce WHERE ce.class_id = c.class_id) * 100.0
           / NULLIF(c.max_student,0)
       AS DECIMAL(5,1)) AS ty_le,
       CASE
           WHEN (SELECT COUNT(*) FROM Class_Enrollment ce WHERE ce.class_id = c.class_id) >= c.max_student THEN N'Đầy'
           WHEN (SELECT COUNT(*) FROM Class_Enrollment ce WHERE ce.class_id = c.class_id) >= c.max_student * 0.8 THEN N'Gần đầy'
           ELSE N'Còn chỗ'
       END AS tinh_trang
FROM Class c;
Câu 12 — Xếp hạng khóa theo doanh thu

Truy vấn sử dụng window function để xếp hạng và tính doanh thu lũy kế.

WITH DoanhThu AS (
    SELECT c.course_id, c.course_name,
           SUM(p.amount) AS doanh_thu
    FROM Course c
    JOIN Enrollment e ON c.course_id = e.course_id
    JOIN Payment p ON e.enrollment_id = p.enrollment_id
    GROUP BY c.course_id, c.course_name
)
SELECT course_name, doanh_thu,
       RANK() OVER (ORDER BY doanh_thu DESC) AS hang,
       SUM(doanh_thu) OVER (ORDER BY doanh_thu DESC) AS luy_ke
FROM DoanhThu;
Câu 13 — Thống kê kỳ thi theo lớp
SELECT c.class_id, c.class_name,
       COUNT(ex.exam_id) AS tong_ky_thi,
       SUM(CASE WHEN ex.exam_date <= GETDATE() THEN 1 ELSE 0 END) AS da_thi,
       SUM(CASE WHEN ex.exam_date > GETDATE() THEN 1 ELSE 0 END) AS chua_thi
FROM Class c
LEFT JOIN Exam ex ON c.class_id = ex.class_id
GROUP BY c.class_id, c.class_name
HAVING COUNT(ex.exam_id) >= 1;
Câu 14 — Skill chưa có lớp
WITH SkillChuaCoLop AS (
    SELECT sk.skill_id, sk.skill_name, sk.course_id
    FROM Skill sk
    WHERE NOT EXISTS (
        SELECT 1 FROM Class c WHERE c.skill_id = sk.skill_id
    )
)
SELECT c.course_name, s.skill_name
FROM SkillChuaCoLop s
JOIN Course c ON s.course_id = c.course_id;
Câu 15 — So sánh điểm giữa kỳ và cuối kỳ
SELECT s.full_name, c.class_name, ex.exam_type, er.overall_score,
       LAG(er.overall_score) OVER (
           PARTITION BY ce.student_id, e_class.class_id
           ORDER BY ex.exam_date
       ) AS diem_truoc,
       er.overall_score - LAG(er.overall_score) OVER (
           PARTITION BY ce.student_id, e_class.class_id
           ORDER BY ex.exam_date
       ) AS muc_tien_bo
FROM Exam_Result er
JOIN Exam ex ON er.exam_id = ex.exam_id
JOIN Class e_class ON ex.class_id = e_class.class_id
JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
JOIN Student s ON ce.student_id = s.student_id
JOIN Class c ON ex.class_id = c.class_id;
Câu 16 — Top phòng học sử dụng nhiều nhất
SELECT r.room_name, c.class_name, sc.study_date, sc.time_slot
FROM Schedule sc
JOIN Room r ON sc.room_id = r.room_id
JOIN Class c ON sc.class_id = c.class_id
WHERE sc.room_id IN (
    SELECT TOP 3 room_id
    FROM Schedule
    GROUP BY room_id
    ORDER BY COUNT(*) DESC
);
Câu 17 — Báo cáo số lượng entity
SELECT N'Học viên' AS loai, status, COUNT(*) FROM Student GROUP BY status
UNION ALL
SELECT N'Giảng viên', status, COUNT(*) FROM Teacher GROUP BY status
UNION ALL
SELECT N'Khóa học', status, COUNT(*) FROM Course GROUP BY status
UNION ALL
SELECT N'Lớp học', status, COUNT(*) FROM Class GROUP BY status
UNION ALL
SELECT N'Phòng học', status, COUNT(*) FROM Room GROUP BY status;
Câu 18 — Xếp hạng giảng viên
WITH DiemTBGV AS (
    SELECT t.teacher_id, t.full_name,
           AVG(er.overall_score) AS diem_tb,
           COUNT(DISTINCT ce.student_id) AS so_hv
    FROM Teacher t
    JOIN Class c ON t.teacher_id = c.teacher_id
    JOIN Exam ex ON c.class_id = ex.class_id
    JOIN Exam_Result er ON ex.exam_id = er.exam_id
    JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
    GROUP BY t.teacher_id, t.full_name
    HAVING COUNT(DISTINCT ce.student_id) >= 3
)
SELECT full_name, diem_tb, so_hv,
       DENSE_RANK() OVER (ORDER BY diem_tb DESC) AS xep_hang
FROM DiemTBGV;
Câu 19 — Lịch học tuần hiện tại
SELECT DISTINCT sc.study_date, sc.time_slot, sc.start_time, sc.end_time,
       c.class_name, t.full_name AS giang_vien,
       r.room_name, r.location
FROM Schedule sc
JOIN Class c ON sc.class_id = c.class_id
JOIN Teacher t ON c.teacher_id = t.teacher_id
JOIN Room r ON sc.room_id = r.room_id;
Câu 20 — Báo cáo điểm theo kỹ năng
WITH DiemChiTiet AS (
    SELECT s.student_id, s.full_name, co.course_name, sk.skill_name,
           AVG(erd.score) AS diem_tb
    FROM Exam_Result_Detailed erd
    JOIN Exam_Result er ON erd.exam_result_id = er.exam_result_id
    JOIN Exam ex ON er.exam_id = ex.exam_id
    JOIN Class c ON ex.class_id = c.class_id
    JOIN Skill sk ON erd.skill_id = sk.skill_id
    JOIN Course co ON sk.course_id = co.course_id
    JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
    JOIN Student s ON ce.student_id = s.student_id
    GROUP BY s.student_id, s.full_name, co.course_name, sk.skill_name
)
SELECT *
FROM DiemChiTiet;