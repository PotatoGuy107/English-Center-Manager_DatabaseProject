import sqlite3
import os

# Lấy đường dẫn chính xác đến file db trong thư mục dự án của Trầm
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "quanlytrungtam.db")


class LoginModel:
    def __init__(self):
        # Tự động "đổ" dữ liệu tài khoản vào DB nếu chưa có
        self.init_account_data()

    def init_account_data(self):
        """Hàm này giúp Trầm không cần mở PyCharm Database mà vẫn có acc để dùng"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Tạo bảng Account nếu DB của Trầm chưa có
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Account (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        """)

        # 2. Kiểm tra nếu chưa có tài khoản nào thì thêm bộ 3 quyền vào
        cursor.execute("SELECT COUNT(*) FROM Account")
        if cursor.fetchone()[0] == 0:
            accounts = [
                ('admin', '123', 'admin'),  # Vào Dashboard
                ('staff', '123', 'staff'),  # Vào Quản lý User
                ('teacher', '123', 'giangvien')  # Vào Teacher View
            ]
            cursor.executemany("INSERT INTO Account VALUES (?, ?, ?)", accounts)
            conn.commit()
        conn.close()

    def check_login(self, username, password):
        """Kiểm tra tài khoản Trầm nhập từ màn hình"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Tìm role dựa trên user và pass
            cursor.execute("SELECT role FROM Account WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Trả về role dưới dạng dictionary cho Controller dùng
                return {"role": result[0]}
            return None
        except Exception as e:
            print(f"Lỗi kết nối DB: {e}")
            return None