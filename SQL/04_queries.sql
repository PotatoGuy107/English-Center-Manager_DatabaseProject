-- 1. Danh sách học viên đang theo học các khóa IELTS
SELECT s.student_id, s.full_name, s.email, 
       c.course_name, e.enrollment_status
FROM Student s
JOIN Enrollment e ON s.student_id = e.student_id
JOIN Course c ON e.course_id = c.course_id
WHERE c.course_name LIKE N'%IELTS%'
ORDER BY s.full_name;
-- 2. Số lượng học viên theo từng khóa học, chỉ hiển thị các khóa có hơn 1 học viên
SELECT c.course_name, COUNT(e.student_id) AS so_hoc_vien
FROM Course c
JOIN Enrollment e ON c.course_id = e.course_id
GROUP BY c.course_name
HAVING COUNT(e.student_id) > 1
ORDER BY so_hoc_vien DESC;
-- 3. Danh sách giáo viên đang giảng dạy các lớp học có trạng thái "Planned"
SELECT teacher_id, full_name, specialization, email
FROM Teacher
WHERE teacher_id IN (
    SELECT DISTINCT teacher_id
    FROM Class
    WHERE status = 'Planned'
);
-- 4. Danh sách học viên chưa thanh toán học phí cho bất kỳ khóa học nào mà họ đã đăng ký
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
-- 5. Danh sách học viên được phân loại theo nhóm tuổi dựa trên ngày sinh của họ
SELECT student_id, full_name, date_of_birth,
    CASE
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) < 12 THEN N'Thiếu nhi'
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) BETWEEN 12 AND 15 THEN N'Thiếu niên'
        WHEN DATEDIFF(YEAR, date_of_birth, GETDATE()) BETWEEN 16 AND 22 THEN N'Thanh niên'
        ELSE N'Trưởng thành'
    END AS nhom_tuoi
FROM Student
ORDER BY date_of_birth;
-- 6. Danh sách học viên cùng với điểm số tổng thể của họ trong các kỳ thi đã tham gia, xếp hạng học viên trong mỗi lớp dựa trên điểm số tổng thể
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
-- 7. Danh sách các lớp học cùng với số lượng học viên đã đăng ký và tổng doanh thu từ các khoản thanh toán cho mỗi lớp
WITH DoanhThuKhoa AS (
    SELECT c.course_id, c.course_name,
           SUM(p.amount) AS tong_doanh_thu,
           COUNT(DISTINCT e.student_id) AS so_hoc_vien
    FROM Course c
    JOIN Enrollment e ON c.course_id = e.course_id
    JOIN Payment p ON e.enrollment_id = p.enrollment_id
    GROUP BY c.course_id, c.course_name
    )
-- 8. Danh sách học viên và giáo viên có địa chỉ email chứa từ khóa "gmail" hoặc "center", phân loại theo vai trò
SELECT full_name, phone_number, email, N'Học viên' AS vai_tro
FROM Student
WHERE email LIKE '%gmail%'

UNION

SELECT full_name, phone_number, email, N'Giảng viên'
FROM Teacher
WHERE email LIKE '%center%'

ORDER BY vai_tro, full_name;
-- 9. Danh sách các phòng học cùng với thông tin về các lớp học được tổ chức trong khoảng thời gian từ ngày 01/01/2025 đến ngày 30/06/2025
SELECT DISTINCT r.room_id, r.room_name, r.capacity, r.location
FROM Room r
JOIN Schedule sc ON r.room_id = sc.room_id
WHERE sc.study_date BETWEEN '2025-01-01' AND '2025-06-30'
ORDER BY r.room_name;
-- 10. Danh sách các giáo viên cùng với số lượng lớp học mà họ đang giảng dạy và tổng số học viên trong các lớp đó, xếp hạng giáo viên dựa trên số lượng lớp học và số học viên
SELECT TOP 5 
    t.teacher_id, t.full_name, t.specialization,
    COUNT(DISTINCT c.class_id) AS so_lop_day,
    COUNT(DISTINCT ce.student_id) AS tong_hoc_vien
FROM Teacher t
JOIN Class c ON t.teacher_id = c.teacher_id
LEFT JOIN Class_Enrollment ce ON c.class_id = ce.class_id
GROUP BY t.teacher_id, t.full_name, t.specialization
ORDER BY so_lop_day DESC, tong_hoc_vien DESC;
-- 11. Danh sách các lớp học cùng với số lượng học viên đã đăng ký, tỷ lệ phần trăm chỗ đã đăng ký so với sức chứa tối đa của lớp, và tình trạng của lớp (đầy, gần đầy, còn chỗ)
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
-- 12. Danh sách các khóa học cùng với tổng doanh thu từ các khoản thanh toán cho mỗi khóa, xếp hạng các khóa học dựa trên doanh thu và tính tổng doanh thu lũy kế
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
-- 13. Danh sách các lớp học cùng với số lượng kỳ thi đã tổ chức, số lượng kỳ thi đã diễn ra và số lượng kỳ thi sắp diễn ra
SELECT c.class_id, c.class_name,
       COUNT(ex.exam_id) AS tong_ky_thi,
       SUM(CASE WHEN ex.exam_date <= GETDATE() THEN 1 ELSE 0 END) AS da_thi,
       SUM(CASE WHEN ex.exam_date > GETDATE() THEN 1 ELSE 0 END) AS chua_thi
FROM Class c
LEFT JOIN Exam ex ON c.class_id = ex.class_id
GROUP BY c.class_id, c.class_name
HAVING COUNT(ex.exam_id) >= 1;
-- 14. Danh sách các khóa học cùng với số lượng kỹ năng được dạy trong mỗi khóa, xếp hạng các khóa học dựa trên số lượng kỹ năng
SELECT c.course_name, sk.skill_name
FROM dbo.Skill sk
JOIN dbo.Course c ON sk.course_id = c.course_id
JOIN dbo.Class cl ON sk.skill_id = cl.skill_id
WHERE cl.class_id IS NoT NULL
-- 15. Danh sách học viên cùng với điểm số tổng thể của họ trong các kỳ thi đã tham gia, điểm số của kỳ thi trước đó (nếu có) và mức tiến bộ giữa các kỳ thi
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
-- 16. Danh sách các phòng học cùng với thông tin về các lớp học được tổ chức trong khoảng thời gian từ ngày 01/01/2025 đến ngày 30/06/2025, chỉ hiển thị các phòng học có số lượng lớp học tổ chức nhiều nhất
SELECT r.room_name, c.class_name, sc.study_date, sc.time_slot
FROM Schedule sc
JOIN Room r ON sc.room_id = r.room_id
JOIN Class c ON sc.class_id = c.class_id
WHERE sc.room_id IN (
    SELECT TOP 3 room_id FROM Schedule
    WHERE study_date BETWEEN '2025-01-01' AND '2025-06-30'
);
-- 17. Danh sách các giáo viên cùng với số lượng lớp học mà họ đang giảng dạy và tổng số học viên trong các lớp đó, xếp hạng giáo viên dựa trên số lượng lớp học và số học viên, chỉ hiển thị các giáo viên có số lượng lớp học và số học viên nhiều nhất
SELECT TOP 5 
    t.full_name, t.specialization,
    COUNT(DISTINCT c.class_id) AS so_lop_day,
    COUNT(DISTINCT ce.student_id) AS tong_hoc_vien,
    RANK() OVER (ORDER BY COUNT(DISTINCT c.class_id) DESC, COUNT(DISTINCT ce.student_id) DESC) AS xep_hang
    FROM Teacher t
    JOIN Class c ON t.teacher_id = c.teacher_id
    LEFT JOIN Class_Enrollment ce ON c.class_id = ce.class_id
    GROUP BY t.teacher_id, t.full_name, t.specialization
    HAVING COUNT(DISTINCT c.class_id) >= ALL (
        SELECT COUNT(DISTINCT c2.class_id)
        FROM Teacher t2
        JOIN Class c2 ON t2.teacher_id = c2.teacher_id
        LEFT JOIN Class_Enrollment ce2 ON c2.class_id = ce2.class_id
        GROUP BY t2.teacher_id
    )
    AND COUNT(DISTINCT ce.student_id) >= ALL (
        SELECT COUNT(DISTINCT ce3.student_id)
        FROM Teacher t3
        JOIN Class c3 ON t3.teacher_id = c3.teacher_id
        LEFT JOIN Class_Enrollment ce3 ON c3.class_id = ce3.class_id
        GROUP BY t3.teacher_id
    )
-- 18. Danh sách các giáo viên cùng với điểm số trung bình của học viên trong các kỳ thi mà họ đã giảng dạy, số lượng học viên đã tham gia kỳ thi và xếp hạng giáo viên dựa trên điểm số trung bình và số lượng học viên
With DiemTrungBinh AS (
    SELECT t.teacher_id, t.full_name, t.specialization,
           AVG(er.overall_score) AS diem_trung_binh,
           COUNT(DISTINCT ce.student_id) AS tong_hoc_vien
    FROM Teacher t
    JOIN Class c ON t.teacher_id = c.teacher_id
    JOIN Exam e ON c.class_id = e.class_id
    JOIN Exam_Result er ON e.exam_id = er.exam_id
    JOIN Class_Enrollment ce ON er.class_enrollment_id = ce.class_enrollment_id
    GROUP BY t.teacher_id, t.full_name, t.specialization
)
SELECT full_name, specialization, diem_trung_binh, tong_hoc_vien,
       RANK() OVER (ORDER BY diem_trung_binh DESC, tong_hoc_vien DESC) AS xep_hang
       FROM DiemTrungBinh
       WHERE diem_trung_binh >= ALL (
           SELECT diem_trung_binh
           FROM DiemTrungBinh
       )
       AND tong_hoc_vien >= ALL (
           SELECT tong_hoc_vien
           FROM DiemTrungBinh
       );
-- 19. Danh sách các lớp học cùng với số lượng học viên đã đăng ký, tỷ lệ phần trăm chỗ đã đăng ký so với sức chứa tối đa của lớp, và tình trạng của lớp (đầy, gần đầy, còn chỗ), chỉ hiển thị các lớp học có tỷ lệ phần trăm chỗ đã đăng ký cao nhất
SELECT DISTINCT sc.study_date, sc.time_slot, sc.start_time, sc.end_time,
       c.class_name, t.full_name AS giang_vien,
       r.room_name, r.location
FROM Schedule sc
JOIN Class c ON sc.class_id = c.class_id
JOIN Teacher t ON c.teacher_id = t.teacher_id
JOIN Room r ON sc.room_id = r.room_id;
-- 20. Danh sách học viên cùng với điểm số chi tiết của họ trong các kỳ thi đã tham gia, bao gồm tên kỹ năng và điểm số của từng kỹ năng, xếp hạng học viên dựa trên điểm số trung bình của tất cả các kỹ năng
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