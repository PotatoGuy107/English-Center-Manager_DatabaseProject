import os
import sqlite3

DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "quanlytrungtam.db")
)


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Course")
    cursor.execute("DROP TABLE IF EXISTS Skill")
    cursor.execute("DROP TABLE IF EXISTS Teacher")
    cursor.execute("DROP TABLE IF EXISTS Room")
    cursor.execute("DROP TABLE IF EXISTS Student")

    cursor.execute("""
        CREATE TABLE Course (
            course_id TEXT PRIMARY KEY,
            course_name TEXT,
            level TEXT,
            fee REAL,
            status TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE Skill (
            skill_id TEXT PRIMARY KEY,
            course_id TEXT,
            skill_name TEXT,
            description TEXT,
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE Teacher (
            teacher_id TEXT PRIMARY KEY,
            full_name TEXT,
            specialization TEXT,
            degree TEXT,
            phone_number TEXT,
            status TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE Room (
            room_id TEXT PRIMARY KEY,
            room_name TEXT,
            capacity INTEGER,
            type TEXT,
            status TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE Student (
            student_id TEXT PRIMARY KEY,
            full_name TEXT,
            phone_number TEXT,
            email TEXT,
            status TEXT
        )
    """)

    # Seed courses
    courses = [
        ("C01", "English Communication", "Beginner", 3500000, "Active"),
        ("C02", "English Communication", "Intermediate", 4000000, "Active"),
        ("C03", "Cambridge Young Learners", "Beginner", 4500000, "Active"),
        ("C04", "Cambridge Young Learners", "Intermediate", 5000000, "Active"),
        ("C05", "IELTS Preparation", "Pre", 6000000, "Active"),
        ("C06", "IELTS Preparation", "Advanced", 7000000, "Active"),
    ]
    cursor.executemany("INSERT INTO Course VALUES (?, ?, ?, ?, ?)", courses)

    # Seed teachers
    teachers = [
        ("T001", "Nguyen Van An", "Listening & Speaking", "Master", "0901000001", "Active"),
        ("T002", "Tran Thi Bich", "Reading & Writing", "Bachelor", "0901000002", "Active"),
        ("T003", "Le Van Cuong", "IELTS", "Master", "0901000003", "Active"),
        ("T004", "Pham Thi Dung", "Cambridge", "Bachelor", "0901000004", "Active"),
        ("T005", "Hoang Van Em", "Listening & Speaking", "Bachelor", "0901000005", "Active"),
        ("T006", "Vo Thi Phuong", "Reading & Writing", "Master", "0901000006", "Active"),
        ("T007", "Nguyen Thi Giang", "IELTS", "PhD", "0901000007", "Active"),
        ("T008", "Dang Van Hung", "Cambridge", "Master", "0901000008", "Active"),
    ]
    cursor.executemany("INSERT INTO Teacher VALUES (?, ?, ?, ?, ?, ?)", teachers)

    # Seed rooms
    rooms = [
        ("R001", "Room 101", 20, "Theory", "Active"),
        ("R002", "Room 102", 15, "Lab", "Active"),
        ("R003", "Room 201", 25, "Theory", "Active"),
    ]
    cursor.executemany("INSERT INTO Room VALUES (?, ?, ?, ?, ?)", rooms)

    # Seed 200 students
    students = [(f"S{i:03d}", f"Student {i:03d}", f"090{i:07d}", f"student{i:03d}@email.com", "Active")
                for i in range(1, 201)]
    cursor.executemany("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", students)

    conn.commit()
    conn.close()
