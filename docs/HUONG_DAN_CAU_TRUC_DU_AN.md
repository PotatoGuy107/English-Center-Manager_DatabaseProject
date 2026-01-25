# 📚 Hướng Dẫn Cấu Trúc Dự Án EnglishCenterManager

---

## 🏗️ Kiến Trúc 3 Tầng

| Tầng | Thư mục | Nhiệm vụ |
|------|---------|----------|
| **Giao diện** | `views/`, `controllers/` | Hiển thị UI, nhận thao tác người dùng |
| **Nghiệp vụ** | `bll/` | Xử lý logic, kiểm tra điều kiện |
| **Dữ liệu** | `dal/` | Đọc/ghi Database |

---

## 📁 Cấu Trúc Thư Mục

```
src/
├── main.py          → Khởi động ứng dụng
├── config/          → Cấu hình kết nối database
├── models/          → Định nghĩa đối tượng (Student, Teacher, Course)
├── views/           → Giao diện người dùng (PyQt6)
├── controllers/     → Điều khiển luồng xử lý
├── bll/             → Xử lý nghiệp vụ, validate dữ liệu
├── dal/             → Truy vấn SQL Server
├── utils/           → Hàm tiện ích dùng chung
└── resources/       → CSS, hình ảnh

tests/               → File kiểm thử
scripts/             → Script tạo database
```

---

## 🔄 Luồng Xử Lý

```
User → View → Controller → BLL → DAL → Database
                                    ↓
User ← View ← Controller ← BLL ← DAL ← (kết quả)
```

---

## 📝 Quy Tắc Quan Trọng

| ✅ NÊN | ❌ KHÔNG |
|--------|----------|
| View chỉ hiển thị | Viết SQL trong View |
| Logic đặt trong BLL | Bỏ qua BLL, gọi thẳng DAL |
| Test trước khi commit | Commit file chứa mật khẩu |

---

## 🚀 Chạy Dự Án

```bash
# 1. Cài môi trường
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Cấu hình database trong src/config/database.py

# 3. Chạy scripts/create_database.sql trong SQL Server

# 4. Khởi động
python src/main.py
```

---

*Cập nhật: 25/01/2026*
