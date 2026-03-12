# English Center Manager Database Project

## 1. Giới thiệu

Đây là hệ thống quản lý trung tâm Anh ngữ, gồm các chức năng:
- Quản lý học viên, giảng viên, khóa học, lớp học, phòng học
- Đăng ký khóa học, ghi danh lớp, quản lý lịch học, kỳ thi, điểm số, thanh toán
- Đăng nhập phân quyền (Admin, Staff, Teacher)

## 2. Cài đặt

### Yêu cầu
- Python >= 3.10
- SQL Server
- Các thư viện: pyodbc, PyQt6


### Tạo và kích hoạt môi trường ảo (virtual environment)

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Cài thư viện
pip install -r requirements.txt
```

### Khởi tạo database
1. Tạo database `EnglishCenterDB` trên SQL Server
2. Chạy các file SQL:
	- `SQL/01_create_table.sql` (tạo bảng)
	- `SQL/02_create_index_table.sql` (tạo index)
	- `SQL/03_insert_sample_data.sql` (dữ liệu mẫu)

## 3. Chạy ứng dụng

```bash
python main.py
```

## 4. Đăng nhập

| Role    | Username   | Password   |
|---------|------------|------------|
| Admin   | admin      | admin123   |
| Staff   | staff1     | staff123   |
| Teacher | teacher_t01| pass123    |

## 5. Chức năng chính
- Dashboard thống kê
- Quản lý học viên, giảng viên, khóa học, lớp học, phòng học
- Đăng ký khóa học, ghi danh lớp
- Quản lý lịch học, kỳ thi, điểm số
- Quản lý thanh toán học phí
- Phân quyền truy cập

## 6. Liên hệ
Nếu có vấn đề, vui lòng liên hệ quản trị viên hoặc gửi issue trên Github.

---
**Chúc bạn sử dụng thành công hệ thống quản lý trung tâm Anh ngữ!**

