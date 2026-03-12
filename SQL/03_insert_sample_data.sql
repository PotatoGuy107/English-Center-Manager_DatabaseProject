INSERT INTO Student ( full_name, date_of_birth, gender, address, phone_number, email, register_date, status) VALUES
( N'Nguyễn Văn An', '2005-03-15', 'Male', N'123 Lê Lợi, Q.1, TP.HCM', '0901234001', 'an.nguyen@gmail.com', '2024-01-10', 'Active'),
( N'Trần Thị Bích', '2006-07-22', 'Female', N'456 Nguyễn Huệ, Q.1, TP.HCM', '0901234002', 'bich.tran@gmail.com', '2024-01-11', 'Active'),
( N'Lê Hoàng Cường', '2004-11-08', 'Male', N'789 Hai Bà Trưng, Q.3, TP.HCM', '0901234003', 'cuong.le@gmail.com', '2024-01-12', 'Active'),
( N'Phạm Thị Dung', '2005-05-30', 'Female', N'321 Võ Văn Tần, Q.3, TP.HCM', '0901234004', 'dung.pham@gmail.com', '2024-01-13', 'Active'),
( N'Hoàng Văn Em', '2007-09-14', 'Male', N'654 Pasteur, Q.1, TP.HCM', '0901234005', 'em.hoang@gmail.com', '2024-01-14', 'Active'),
( N'Võ Thị Phương', '2006-02-28', 'Female', N'987 Nam Kỳ Khởi Nghĩa, Q.3, TP.HCM', '0901234006', 'phuong.vo@gmail.com', '2024-01-15', 'Active'),
( N'Nguyễn Thị Giang', '2005-12-01', 'Female', N'147 Điện Biên Phủ, Bình Thạnh', '0901234007', 'giang.nguyen@gmail.com', '2024-01-16', 'Active'),
( N'Đặng Văn Hùng', '2004-06-17', 'Male', N'258 Nguyễn Đình Chiểu, Q.3, TP.HCM', '0901234008', 'hung.dang@gmail.com', '2024-01-17', 'Active'),
( N'Bùi Thị Ý', '2006-10-25', 'Female', N'369 Cách Mạng Tháng 8, Q.10, TP.HCM', '0901234009', 'y.bui@gmail.com', '2024-01-18', 'Active'),
( N'Trịnh Văn Khoa', '2005-04-05', 'Male', N'741 Lý Thường Kiệt, Q.10, TP.HCM', '0901234010', 'khoa.trinh@gmail.com', '2024-01-19', 'Active'),
( N'Lý Thị Lan', '2007-08-19', 'Female', N'852 Trần Hưng Đạo, Q.5, TP.HCM', '0901234011', 'lan.ly@gmail.com', '2024-01-20', 'Active'),
( N'Ngô Văn Minh', '2004-01-23', 'Male', N'963 Nguyễn Tri Phương, Q.10, TP.HCM', '0901234012', 'minh.ngo@gmail.com', '2024-01-21', 'Active'),
( N'Đinh Thị Ngọc', '2006-05-11', 'Female', N'159 Lê Hồng Phong, Q.10, TP.HCM', '0901234013', 'ngoc.dinh@gmail.com', '2024-01-22', 'Active'),
( N'Vũ Văn Phúc', '2005-09-29', 'Male', N'267 Sư Vạn Hạnh, Q.10, TP.HCM', '0901234014', 'phuc.vu@gmail.com', '2024-01-23', 'Active'),
( N'Hồ Thị Quỳnh', '2007-03-07', 'Female', N'378 Lý Tự Trọng, Q.1, TP.HCM', '0901234015', 'quynh.ho@gmail.com', '2024-01-24', 'Active'),
( N'Phan Văn Sơn', '2004-07-16', 'Male', N'489 Nguyễn Thị Minh Khai, Q.1, TP.HCM', '0901234016', 'son.phan@gmail.com', '2024-01-25', 'Active'),
( N'Mai Thị Trang', '2006-11-03', 'Female', N'591 Bùi Viện, Q.1, TP.HCM', '0901234017', 'trang.mai@gmail.com', '2024-01-26', 'Active'),
( N'Dương Văn Uy', '2005-02-14', 'Male', N'693 Phạm Ngũ Lão, Q.1, TP.HCM', '0901234018', 'uy.duong@gmail.com', '2024-01-27', 'Active'),
( N'Cao Thị Vân', '2007-06-21', 'Female', N'795 Đề Thám, Q.1, TP.HCM', '0901234019', 'van.cao@gmail.com', '2024-01-28', 'Active'),
( N'Tô Văn Xuân', '2004-10-09', 'Male', N'897 Cống Quỳnh, Q.1, TP.HCM', '0901234020', 'xuan.to@gmail.com', '2024-01-29', 'Active');
GO

INSERT INTO Teacher (full_name, phone_number, email, specialization, hire_date, status) VALUES
(N'Nguyễn Minh Anh', '0912000001', 'anh.nguyen@center.edu.vn', N'IELTS Speaking', '2020-01-15', 'Active'),
(N'Trần Thu Hằng', '0912000002', 'hang.tran@center.edu.vn', N'IELTS Writing', '2020-03-20', 'Active'),
(N'Lê Văn Cương', '0912000003', 'cuong.le@center.edu.vn', N'IELTS Listening', '2019-06-01', 'Active'),
(N'Phạm Thị Diệu', '0912000004', 'dieu.pham@center.edu.vn', N'IELTS Reading', '2021-02-10', 'Active'),
(N'Hoàng Đức Em', '0912000005', 'em.hoang@center.edu.vn', N'Cambridge Starters', '2022-01-05', 'Active'),
(N'Võ Thị Phượng', '0912000006', 'phuong.vo@center.edu.vn', N'Cambridge Movers', '2018-09-12', 'Active'),
(N'Nguyễn Thị Giao', '0912000007', 'giao.nguyen@center.edu.vn', N'Cambridge Flyers', '2017-04-25', 'Active'),
(N'Đặng Minh Hải', '0912000008', 'hai.dang@center.edu.vn', N'TOEIC', '2023-01-01', 'Active'),
(N'Bùi Hoàng Ý', '0912000009', 'y.bui@center.edu.vn', N'Giao tiếp cơ bản', '2019-08-15', 'Active'),
(N'Trịnh Văn Kiên', '0912000010', 'kien.trinh@center.edu.vn', N'Giao tiếp nâng cao', '2020-05-22', 'Active'),
(N'Lý Thị Liên', '0912000011', 'lien.ly@center.edu.vn', N'Business English', '2018-11-30', 'Active'),
(N'Ngô Anh Minh', '0912000012', 'minh.ngo@center.edu.vn', N'IELTS Speaking', '2021-07-18', 'Active'),
(N'Đinh Thị Nhung', '0912000013', 'nhung.dinh@center.edu.vn', N'IELTS Writing', '2022-04-09', 'Active'),
(N'Vũ Hoàng Phong', '0912000014', 'phong.vu@center.edu.vn', N'Grammar', '2019-12-05', 'Active'),
(N'Hồ Thị Quyên', '0912000015', 'quyen.ho@center.edu.vn', N'Pronunciation', '2020-09-28', 'Active'),
(N'Phan Văn Sang', '0912000016', 'sang.phan@center.edu.vn', N'TOEFL', '2017-06-14', 'Active'),
(N'Mai Kim Thảo', '0912000017', 'thao.mai@center.edu.vn', N'Kids English', '2023-03-21', 'Active'),
(N'Dương Văn Ước', '0912000018', 'uoc.duong@center.edu.vn', N'Academic Writing', '2018-02-07', 'Active'),
(N'Cao Thị Vy', '0912000019', 'vy.cao@center.edu.vn', N'Conversation', '2021-10-16', 'Active'),
(N'Tô Minh Xuân', '0912000020', 'xuan.to@center.edu.vn', N'IELTS Overall', '2019-04-02', 'Active');
GO
select * from Teacher

INSERT INTO Course (course_name, description, level, duration_weeks, tuition_fee, status) VALUES
(N'English Communication Basic', N'Khóa giao tiếp tiếng Anh cơ bản cho người mới bắt đầu', 'Beginner', 12, 3500000, 'Active'),
(N'English Communication Intermediate', N'Khóa giao tiếp tiếng Anh trung cấp', 'Intermediate', 16, 4500000, 'Active'),
(N'English Communication Advanced', N'Khóa giao tiếp tiếng Anh nâng cao', 'Advanced', 16, 5500000, 'Active'),
(N'Cambridge Starters', N'Luyện thi Cambridge Starters cho trẻ em 7-9 tuổi', 'Beginner', 20, 4000000, 'Active'),
(N'Cambridge Movers', N'Luyện thi Cambridge Movers cho trẻ em 8-11 tuổi', 'Elementary', 20, 4500000, 'Active'),
(N'Cambridge Flyers', N'Luyện thi Cambridge Flyers cho trẻ em 9-12 tuổi', 'Intermediate', 24, 5000000, 'Active'),
(N'IELTS Foundation', N'Khóa nền tảng IELTS mục tiêu 5.0-5.5', 'Pre-IELTS', 16, 6000000, 'Active'),
(N'IELTS Intensive', N'Khóa IELTS chuyên sâu mục tiêu 6.0-7.0', 'Advanced', 20, 8000000, 'Active');
GO
select * from Course

INSERT INTO Skill (course_id, skill_name, description) VALUES
-- Communication Basic (16)
(16, N'Basic Listening', N'Kỹ năng nghe cơ bản'),
(16, N'Basic Speaking', N'Kỹ năng nói cơ bản'),
(16, N'Basic Reading', N'Kỹ năng đọc cơ bản'),

-- Communication Intermediate (17)
(17, N'Intermediate Listening', N'Kỹ năng nghe trung cấp'),
(17, N'Intermediate Speaking', N'Kỹ năng nói trung cấp'),
(17, N'Intermediate Writing', N'Kỹ năng viết trung cấp'),

-- Communication Advanced (18)
(18, N'Advanced Listening', N'Kỹ năng nghe nâng cao'),
(18, N'Advanced Speaking', N'Kỹ năng nói nâng cao'),

-- Cambridge Starters (19)
(19, N'Starters Listening', N'Nghe Cambridge Starters'),
(19, N'Starters Speaking', N'Nói Cambridge Starters'),
(19, N'Starters Reading & Writing', N'Đọc viết Cambridge Starters'),

-- Cambridge Movers (20)
(20, N'Movers Listening', N'Nghe Cambridge Movers'),
(20, N'Movers Speaking', N'Nói Cambridge Movers'),
(20, N'Movers Reading & Writing', N'Đọc viết Cambridge Movers'),

-- Cambridge Flyers (21)
(21, N'Flyers Listening', N'Nghe Cambridge Flyers'),
(21, N'Flyers Speaking', N'Nói Cambridge Flyers'),
(21, N'Flyers Reading & Writing', N'Đọc viết Cambridge Flyers'),

-- IELTS Foundation (22)
(22, N'IELTS Listening 5.0', N'Luyện nghe IELTS mục tiêu 5.0'),
(22, N'IELTS Speaking 5.0', N'Luyện nói IELTS mục tiêu 5.0'),
(22, N'IELTS Reading 5.0', N'Luyện đọc IELTS mục tiêu 5.0'),
(22, N'IELTS Writing 5.0', N'Luyện viết IELTS mục tiêu 5.0'),

-- IELTS Intensive (23)
(23, N'IELTS Intensive All Skills', N'Luyện 4 kỹ năng IELTS chuyên sâu');


INSERT INTO Room (room_name, capacity, location, status) VALUES
(N'Phòng 101', 20, N'Tầng 1 - Tòa A', 'available'),
(N'Phòng 102', 20, N'Tầng 1 - Tòa A', 'available'),
(N'Phòng 103', 15, N'Tầng 1 - Tòa A', 'available'),
(N'Phòng 104', 15, N'Tầng 1 - Tòa A', 'available'),
(N'Phòng 201', 25, N'Tầng 2 - Tòa A', 'available'),
(N'Phòng 202', 25, N'Tầng 2 - Tòa A', 'available'),
(N'Phòng 203', 30, N'Tầng 2 - Tòa A', 'available'),
(N'Phòng 204', 30, N'Tầng 2 - Tòa A', 'available'),
(N'Phòng 301', 20, N'Tầng 3 - Tòa A', 'available'),
(N'Phòng 302', 20, N'Tầng 3 - Tòa A', 'available'),
(N'Phòng Lab 1', 18, N'Tầng 3 - Tòa B', 'available'),
(N'Phòng Lab 2', 18, N'Tầng 3 - Tòa B', 'available'),
(N'Phòng Lab 3', 18, N'Tầng 3 - Tòa B', 'available'),
(N'Phòng VIP 1', 10, N'Tầng 4 - Tòa A', 'available'),
(N'Phòng VIP 2', 10, N'Tầng 4 - Tòa A', 'available'),
(N'Phòng Speaking 1', 8, N'Tầng 4 - Tòa B', 'available'),
(N'Phòng Speaking 2', 8, N'Tầng 4 - Tòa B', 'available'),
(N'Hội trường A', 50, N'Tầng 1 - Tòa B', 'available'),
(N'Hội trường B', 40, N'Tầng 2 - Tòa B', 'available'),
(N'Phòng thi', 35, N'Tầng 1 - Tòa B', 'available');
GO
select * from Room

INSERT INTO Class (class_name, skill_id, teacher_id, start_date, end_date, max_student, status) VALUES

(N'Giao tiếp CB - Nghe A1', 18, 27, '2024-01-15', '2024-04-15', 20, 'Planned'),
(N'Giao tiếp CB - Nói A1', 19, 28, '2024-01-15', '2024-04-15', 20, 'Planned'),
(N'Giao tiếp CB - Đọc A1', 20, 37, '2024-01-20', '2024-04-20', 18, 'Planned'),

(N'Giao tiếp TC - Nghe B1', 21, 27, '2024-02-01', '2024-06-01', 18, 'Planned'),
(N'Giao tiếp TC - Nói B1', 22, 28, '2024-02-01', '2024-06-01', 18, 'Planned'),
(N'Giao tiếp TC - Viết B1', 23, 36, '2024-02-01', '2024-06-01', 15, 'Planned'),

(N'Giao tiếp NC - Nghe C1', 24, 37, '2024-03-01', '2024-07-01', 15, 'Planned'),
(N'Giao tiếp NC - Nói C1', 25, 29, '2024-03-01', '2024-07-01', 15, 'Planned'),

(N'Cambridge Starters - Nghe', 26, 23, '2024-01-10', '2024-06-10', 15, 'Planned'),
(N'Cambridge Starters - Nói', 27, 35, '2024-01-10', '2024-06-10', 12, 'Planned'),

(N'Cambridge Movers - Nghe', 29, 24, '2024-02-15', '2024-07-15', 15, 'Planned'),
(N'Cambridge Movers - Nói', 30, 35, '2024-02-15', '2024-07-15', 12, 'Planned'),

(N'Cambridge Flyers - Nghe', 32, 25, '2024-03-01', '2024-09-01', 15, 'Planned'),
(N'Cambridge Flyers - Nói', 33, 25, '2024-03-01', '2024-09-01', 12, 'Planned'),

(N'IELTS 5.0 - Listening', 35, 21, '2024-01-20', '2024-05-20', 18, 'Planned'),
(N'IELTS 5.0 - Speaking', 36, 19, '2024-01-20', '2024-05-20', 12, 'Planned'),
(N'IELTS 5.0 - Reading', 37, 22, '2024-01-20', '2024-05-20', 18, 'Planned'),
(N'IELTS 5.0 - Writing', 38, 20, '2024-01-20', '2024-05-20', 15, 'Planned'),

(N'IELTS 6.0+ Intensive', 39, 38, '2024-02-01', '2024-07-01', 15, 'Planned'),
(N'IELTS 6.0+ Intensive B', 39, 30, '2024-03-01', '2024-08-01', 15, 'Planned');
GO

INSERT INTO Enrollment (student_id, course_id, enrollment_date, start_date, end_date, enrollment_status) VALUES
(1,16,'2024-01-10','2024-01-15','2024-04-15','studying'),
(2,16,'2024-01-11','2024-01-15','2024-04-15','studying'),
(3,16,'2024-01-12','2024-01-15','2024-04-15','studying'),
(4,17,'2024-01-28','2024-02-01','2024-06-01','studying'),
(5,17,'2024-01-29','2024-02-01','2024-06-01','studying'),
(6,18,'2024-02-25','2024-03-01','2024-07-01','studying'),
(7,19,'2024-01-05','2024-01-10','2024-06-10','studying'),
(8,19,'2024-01-06','2024-01-10','2024-06-10','studying'),
(9,20,'2024-02-10','2024-02-15','2024-07-15','studying'),
(10,20,'2024-02-12','2024-02-15','2024-07-15','studying'),
(11,21,'2024-02-26','2024-03-01','2024-09-01','studying'),
(12,21,'2024-02-27','2024-03-01','2024-09-01','studying'),
(13,22,'2024-01-15','2024-01-20','2024-05-20','studying'),
(14,22,'2024-01-16','2024-01-20','2024-05-20','studying'),
(15,22,'2024-01-17','2024-01-20','2024-05-20','studying'),
(16,23,'2024-01-25','2024-02-01','2024-07-01','studying'),
(17,23,'2024-01-26','2024-02-01','2024-07-01','studying'),
(18,23,'2024-02-25','2024-03-01','2024-08-01','studying'),
(19,16,'2024-01-13','2024-01-15','2024-04-15','studying'),
(20,17,'2024-01-30','2024-02-01','2024-06-01','studying');

