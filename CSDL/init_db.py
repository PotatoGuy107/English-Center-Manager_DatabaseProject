import sqlite3

def tao_database_moi():
    conn = sqlite3.connect("quanlytrungtam.db")
    cursor = conn.cursor()

    # --- 1. BẢNG COURSE (Khóa học) ---
    cursor.execute("DROP TABLE IF EXISTS Course")
    cursor.execute('''
        CREATE TABLE Course (
            course_id TEXT PRIMARY KEY,
            course_name TEXT,
            level TEXT,
            fee TEXT,
            status TEXT
        )
    ''')
    courses = [
        ('C01', 'Eng Comm Basic', 'Basic', '3.000.000', 'Active'),
        ('C02', 'English Starter', 'Starter', '2.500.000', 'Active'),
        ('C03', 'Cambridge Mover', 'Mover', '3.500.000', 'Active'),
        ('C04', 'Cambridge Flyer', 'Flyer', '4.000.000', 'Active'),
        ('C05', 'IELTS 5.0', 'IELTS', '6.000.000', 'Active'),
        ('C06', 'IELTS 6.0', 'IELTS', '8.000.000', 'Active')
    ]
    cursor.executemany("INSERT INTO Course VALUES (?, ?, ?, ?, ?)", courses)

    # --- 2. BẢNG SKILL (Kỹ năng - Dùng cho hiệu ứng Hover) ---
    cursor.execute("DROP TABLE IF EXISTS Skill")
    cursor.execute('''
        CREATE TABLE Skill (
            skill_id TEXT PRIMARY KEY,
            course_id TEXT,
            skill_name TEXT,
            description TEXT
        )
    ''')
    skills_data = [
        ('S01', 'C01', 'Communication Listening', 'Listening skills for Communication'),
        ('S02', 'C01', 'Communication Speaking', 'Speaking skills for Communication'),
        ('S03', 'C02', 'Basic Listening', 'Basic Listening for beginners'),
        ('S04', 'C02', 'Basic Speaking', 'Basic Speaking for beginners'),
        ('S05', 'C02', 'Basic Reading', 'Basic Reading for beginners'),
        ('S06', 'C02', 'Basic Writing', 'Basic Writing for beginners'),
        ('S07', 'C03', 'Listening', 'Listening skills for Cambridge Mover'),
        ('S08', 'C03', 'Speaking', 'Speaking skills for Cambridge Mover'),
        ('S09', 'C03', 'Reading', 'Reading skills for Cambridge Mover'),
        ('S10', 'C03', 'Writing', 'Writing skills for Cambridge Mover'),
        ('S11', 'C04', 'Listening', 'Listening skills for Cambridge Flyer'),
        ('S12', 'C04', 'Speaking', 'Speaking skills for Cambridge Flyer'),
        ('S13', 'C04', 'Reading', 'Reading skills for Cambridge Flyer'),
        ('S14', 'C04', 'Writing', 'Writing skills for Cambridge Flyer'),
        ('S15', 'C05', 'Listening', 'Listening skills for IELTS 5.0'),
        ('S16', 'C05', 'Speaking', 'Speaking skills for IELTS 5.0'),
        ('S17', 'C05', 'Reading', 'Reading skills for IELTS 5.0'),
        ('S18', 'C05', 'Writing', 'Writing skills for IELTS 5.0'),
        ('S19', 'C06', 'Listening', 'Listening skills for IELTS 6.0'),
        ('S20', 'C06', 'Speaking', 'Speaking skills for IELTS 6.0'),
        ('S21', 'C06', 'Reading', 'Reading skills for IELTS 6.0'),
        ('S22', 'C06', 'Writing', 'Writing skills for IELTS 6.0')
    ]
    cursor.executemany("INSERT INTO Skill VALUES (?, ?, ?, ?)", skills_data)

    # --- 3. BẢNG TEACHER (Giảng viên) ---
    cursor.execute("DROP TABLE IF EXISTS Teacher")
    cursor.execute('''
        CREATE TABLE Teacher (
            teacher_id TEXT PRIMARY KEY,
            full_name TEXT,
            specialization TEXT,
            degree TEXT,
            phone_number TEXT,
            status TEXT
        )
    ''')
    teachers = [
        ('T01', 'Nguyen Van A', 'IELTS', 'Master', '0901234567', 'Active'),
        ('T02', 'Tran Thi B', 'Communication', 'Bachelor', '0902345678', 'Active'),
        ('T03', 'Le Van C', 'Cambridge', 'PhD', '0903456789', 'Active'),
        ('T04', 'Pham Thi D', 'IELTS', 'Master', '0904567890', 'Active'),
        ('T05', 'Hoang Van E', 'Communication', 'Bachelor', '0905678901', 'Active'),
        ('T06', 'Vu Thi F', 'Cambridge', 'Master', '0906789012', 'Active'),
        ('T07', 'Dang Van G', 'IELTS', 'Bachelor', '0907890123', 'Active'),
        ('T08', 'Bui Thi H', 'Communication', 'Master', '0908901234', 'Active')
    ]
    cursor.executemany("INSERT INTO Teacher VALUES (?, ?, ?, ?, ?, ?)", teachers)

    # --- 4. BẢNG ROOM (Phòng học) ---
    cursor.execute("DROP TABLE IF EXISTS Room")
    cursor.execute('''
        CREATE TABLE Room (
            room_id TEXT PRIMARY KEY,
            room_name TEXT,
            capacity INTEGER,
            type TEXT,
            status TEXT
        )
    ''')
    rooms = [
        ('R01', 'Phòng A1', 30, 'Lý thuyết', 'Active'),
        ('R02', 'Phòng Lab 1', 25, 'Thực hành', 'Active'),
        ('R03', 'Phòng Hội thảo', 50, 'Đa năng', 'Active')
    ]
    cursor.executemany("INSERT INTO Room VALUES (?, ?, ?, ?, ?)", rooms)

    # --- 5. BẢNG STUDENT (Học viên - Tạo 200 học viên giả lập) ---
    cursor.execute("DROP TABLE IF EXISTS Student")
    cursor.execute('''
        CREATE TABLE Student (
            student_id TEXT PRIMARY KEY,
            full_name TEXT,
            phone_number TEXT,
            email TEXT,
            status TEXT
        )
    ''')
    students = []
    for i in range(1, 201):
        students.append((f'S{i:03d}', f'Học viên {i}', f'0912345{i:03d}', f'student{i}@example.com', 'Active'))
    cursor.executemany("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", students)

    conn.commit()
    conn.close()
    print(">>> ĐÃ CẬP NHẬT FULL DATA: 6 Khóa học, 22 Kỹ năng, 8 Giảng viên, 200 Học viên, 3 Phòng học.")

if __name__ == "__main__":
    tao_database_moi()