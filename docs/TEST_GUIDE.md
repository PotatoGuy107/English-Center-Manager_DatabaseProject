# Hướng dẫn Test Chức năng - English Center Manager

## Thông tin đăng nhập

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| staff | staff123 | Staff |
| teacher | teacher123 | Teacher |

---

## 1. QUẢN LÝ PHÒNG HỌC (Room Management)

### Quy tắc Database:
- **Room ID**: Tự sinh (INT IDENTITY) - KHÔNG nhập thủ công
- **Status**: Chỉ chấp nhận 3 giá trị: `available`, `maintenance`, `unavailable`

### Test Case 1.1: Xem danh sách phòng
- **Bước thực hiện**: Đăng nhập → Vào "Quản lý phòng học"
- **Kết quả mong đợi**: Hiển thị bảng với các cột: Mã phòng, Tên phòng, Sức chứa, Vị trí, Trạng thái
- **Dữ liệu mẫu**: 1 - Phòng 101, 25, Tầng 1, available

### Test Case 1.2: Thêm phòng mới
- **Bước thực hiện**: 
  1. Click nút "Thêm"
  2. Room ID hiển thị "(Auto)" - KHÔNG NHẬP
  3. Nhập: Tên phòng = "Phòng 301", Sức chứa = "35", Vị trí = "Tầng 3"
  4. Chọn Trạng thái từ dropdown: `available`
  5. Click OK
- **Kết quả mong đợi**: 
  - Phòng mới được thêm với mã số tự động (7, 8, 9...)
  - Thông báo "Room 7 added successfully!"

### Test Case 1.3: Đóng/Mở phòng
- **Bước thực hiện**: Chọn 1 phòng → Click "Đóng/Mở"
- **Kết quả mong đợi**: Trạng thái chuyển từ `available` ↔ `unavailable`

---

## 2. QUẢN LÝ GIÁO VIÊN (Teacher Management)

### Quy tắc Database:
- **Teacher ID**: Tự sinh (INT IDENTITY) - KHÔNG nhập thủ công
- **Status**: Giá trị mặc định "Active"

### Test Case 2.1: Xem danh sách giáo viên
- **Bước thực hiện**: Đăng nhập → Vào "Quản lý giáo viên"
- **Kết quả mong đợi**: Hiển thị bảng với các cột: Mã GV, Họ tên, SĐT, Email, Chuyên môn, Ngày vào, Trạng thái
- **Dữ liệu mẫu**: 1 - Nguyễn Minh Anh, 0901111111, anh.nguyen@center.com, Giao tiếp, Active

### Test Case 2.2: Thêm giáo viên mới
- **Bước thực hiện**:
  1. Click nút "Thêm"
  2. ID hiển thị "(Auto)" - KHÔNG NHẬP
  3. Nhập:
     - Họ tên: "Trần Văn Test"
     - SĐT: "0909999999"
     - Email: "test@center.com"
     - Chuyên môn: "IELTS"
     - Ngày vào: để trống (tự điền hôm nay)
     - Trạng thái: "Active"
  4. Click OK
- **Kết quả mong đợi**: 
  - Mã giáo viên tự sinh (9, 10, 11...)
  - Thông báo "Teacher 9 added successfully!"

### Test Case 2.3: Sửa thông tin giáo viên
- **Bước thực hiện**: Chọn 1 giáo viên → Click "Sửa" → Đổi SĐT → OK
- **Kết quả mong đợi**: Thông tin được cập nhật trong bảng

### Test Case 2.4: Xóa giáo viên
- **Bước thực hiện**: Chọn 1 giáo viên → Click "Xóa" → Xác nhận
- **Kết quả mong đợi**: Giáo viên bị xóa khỏi danh sách
- **Lưu ý**: Không xóa được giáo viên đang dạy lớp (FK constraint)

---

## 3. QUẢN LÝ KHÓA HỌC (Course Management)

### Quy tắc Database:
- **Course ID**: Tự sinh (INT IDENTITY) - KHÔNG nhập thủ công

### Test Case 3.1: Xem danh sách khóa học
- **Bước thực hiện**: Đăng nhập → Vào "Quản lý khóa học"
- **Kết quả mong đợi**: Hiển thị các khóa: 1-IELTS 6.0, 2-English Starter, etc.

### Test Case 3.2: Thêm khóa học mới
- **Bước thực hiện**:
  1. Click "Thêm"
  2. ID hiển thị "(Auto)" - KHÔNG NHẬP
  3. Nhập:
     - Course Name: "TOEIC 600"
     - Description: "Khóa học luyện thi TOEIC"
     - Level: chọn "Intermediate"
     - Duration: 12 weeks
     - Tuition Fee: 5,000,000 VND
     - Status: "Active"
  4. OK
- **Kết quả mong đợi**: 
  - Khóa học mới với mã tự sinh (7, 8, 9...)
  - Thông báo "Course 7 added!"

---

## 4. QUẢN LÝ LỚP HỌC (Class Management)

### Test Case 4.1: Xem danh sách lớp
- **Bước thực hiện**: Đăng nhập → Vào "Quản lý lớp học"
- **Kết quả mong đợi**: Hiển thị bảng lớp với: Mã lớp, Tên lớp, Khóa học, Kỹ năng, Giáo viên, Ngày bắt đầu, Ngày kết thúc, Sĩ số tối đa, Trạng thái

### Test Case 4.2: Tạo lớp mới
- **Bước thực hiện**:
  1. Click "Tạo lớp"
  2. Nhập:
     - Tên lớp: "Lớp Test IELTS"
     - Khóa học: Chọn từ dropdown
     - Kỹ năng: Chọn từ dropdown  
     - Giáo viên: Chọn từ dropdown
     - Ngày bắt đầu: 2026-04-01
     - Ngày kết thúc: 2026-06-30
     - Sĩ số tối đa: 25
  3. Click Lưu
- **Kết quả mong đợi**: 
  - Mã lớp tự sinh (CL23, CL24...)
  - Lớp mới xuất hiện trong danh sách

### Test Case 4.3: Xem chi tiết lớp
- **Bước thực hiện**: Click vào 1 lớp trong bảng
- **Kết quả mong đợi**: Hiển thị thông tin chi tiết, danh sách học viên, lịch học

---

## 5. QUẢN LÝ HỌC VIÊN (Student Management)

### Test Case 5.1: Thêm học viên vào lớp
- **Bước thực hiện**:
  1. Chọn 1 lớp → Vào "Danh sách học viên"
  2. Click "Thêm học viên"
  3. Nhập:
     - Họ tên: "Học viên Test"
     - Ngày sinh: 2000-01-01
     - Giới tính: Male
     - Địa chỉ: "Quận 1, TP.HCM"
     - SĐT: "0912345678"
     - Email: "hocvien@test.com"
  4. Lưu
- **Kết quả mong đợi**:
  - Mã học viên tự sinh (ST201, ST202...)
  - Tự động ghi danh vào lớp (Class_Enrollment)

### Test Case 5.2: Tìm kiếm học viên
- **Bước thực hiện**: Nhập từ khóa vào ô tìm kiếm (tên hoặc mã)
- **Kết quả mong đợi**: Lọc danh sách theo từ khóa

---

## 6. DATABASE - Kiểm tra dữ liệu

### Chạy truy vấn SQL Server:

```sql
-- Kiểm tra students
SELECT * FROM Student WHERE student_id LIKE 'ST2%';

-- Kiểm tra teachers  
SELECT * FROM Teacher;

-- Kiểm tra rooms
SELECT * FROM Room;

-- Kiểm tra classes
SELECT * FROM Class;

-- Kiểm tra class enrollments
SELECT ce.*, s.full_name, c.class_name 
FROM Class_Enrollment ce
JOIN Student s ON ce.student_id = s.student_id
JOIN Class c ON ce.class_id = c.class_id;

-- Kiểm tra payments
SELECT p.*, e.student_id, s.full_name
FROM Payment p
JOIN Enrollment e ON p.enrollment_id = e.enrollment_id
JOIN Student s ON e.student_id = s.student_id;
```

---

## 7. EDGE CASES VÀ LỖI CẦN TEST

### 7.1 Validation
- [ ] Thêm giáo viên với email trống → Có báo lỗi?
- [ ] Thêm lớp với ngày kết thúc < ngày bắt đầu → Có báo lỗi?
- [ ] Nhập số âm cho sức chứa phòng → Có validate?

### 7.2 CHECK Constraints
- [ ] Room status chỉ được chọn: `available`, `maintenance`, `unavailable` (dropdown)
- [ ] Nhập sai status → Lỗi CHECK constraint

### 7.3 Foreign Key Constraints
- [ ] Xóa khóa học đang có lớp → Phải báo lỗi (FK constraint)
- [ ] Xóa giáo viên đang dạy lớp → Phải báo lỗi
- [ ] Xóa học viên đang trong lớp → Cần xóa Class_Enrollment trước

### 7.4 Date Format
- [ ] Các ngày hiển thị đúng format YYYY-MM-DD
- [ ] Chọn ngày từ DatePicker lưu đúng vào database

---

## 8. CHECKLIST TEST NHANH

| # | Chức năng | Thao tác | Kết quả |
|---|-----------|----------|---------|
| 1 | Đăng nhập | admin/admin123 | ☐ OK |
| 2 | Xem phòng | Vào Quản lý phòng | ☐ OK |
| 3 | Thêm phòng | Tên, Sức chứa, Vị trí, Status=`available` | ☐ OK |
| 4 | Toggle phòng | Chọn phòng → Đóng/Mở | ☐ OK |
| 5 | Xem GV | Vào Quản lý GV | ☐ OK |
| 6 | Thêm GV | Nhập info → Save | ☐ OK |
| 7 | Sửa GV | Chọn → Sửa → Save | ☐ OK |
| 8 | Xem khóa học | Vào Quản lý KH | ☐ OK |
| 9 | Thêm khóa học | Nhập → Save | ☐ OK |
| 10 | Xem lớp | Vào Quản lý lớp | ☐ OK |
| 11 | Tạo lớp mới | Fill form → Save | ☐ OK |
| 12 | Thêm HV vào lớp | Chọn lớp → Thêm HV | ☐ OK |
| 13 | Đăng xuất | Click Logout | ☐ OK |

---

## 9. HƯỚNG DẪN CHẠY ỨNG DỤNG

```powershell
# 1. Activate venv (nếu có)
cd "d:\CODE\CSDL\English-Center-Manager_DatabaseProject"

# 2. Chạy main.py
python main.py
```

### Yêu cầu:
- Python 3.10+
- PyQt6
- pyodbc
- python-dotenv
- SQL Server với database EnglishCenterDB đã seed data

### File .env:
```
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=MSI
DB_DATABASE=EnglishCenterDB
DB_USER=sa
DB_PASSWORD=123456
```

---

## 10. BÁO CÁO LỖI

Nếu gặp lỗi, ghi lại:
1. Chức năng đang test
2. Các bước thực hiện
3. Thông báo lỗi (screenshot nếu có)
4. Terminal output (nếu có)

**Lỗi thường gặp:**
- "No module named 'dotenv'" → `pip install python-dotenv`
- Connection error → Kiểm tra SQL Server đang chạy và .env đúng
- FK constraint error → Có dữ liệu liên quan chưa xóa
