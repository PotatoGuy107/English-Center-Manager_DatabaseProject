import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from .env
DB_SERVER = os.getenv("DB_SERVER", "localhost").strip()
DB_PORT = os.getenv("DB_PORT", "1433").strip()
DB_DATABASE = os.getenv("DB_DATABASE", "EnglishCenterDB").strip()
DB_USER = os.getenv("DB_USER", "sa").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").strip()


def get_connection_string():
    """Build SQL Server connection string"""
    if DB_USER and DB_PASSWORD:
        # SQL Server Authentication
        return (
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )
    else:
        # Windows Authentication
        return (
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"Trusted_Connection=yes;"
        )


def get_connection():
    """Get database connection to SQL Server"""
    try:
        conn = pyodbc.connect(get_connection_string())
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        raise


def test_connection():
    """Test if database connection works"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def execute_query(query: str, params: tuple = None) -> list:
    """Execute SELECT query and return results"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        conn.close()


def execute_non_query(query: str, params: tuple = None) -> bool:
    """Execute INSERT, UPDATE, DELETE queries"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except pyodbc.Error as e:
        print(f"Query execution error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def execute_scalar(query: str, params: tuple = None):
    """Execute query and return single value"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def init_seed_data():
    """Insert seed data into SQL Server database (assumes tables already exist from SQL scripts)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM Course")
        if cursor.fetchone()[0] > 0:
            print("Seed data already exists. Skipping...")
            conn.close()
            return
        
        # Seed courses
        courses = [
            ("C01", "English Communication", "Basic English communication skills", "Beginner", 12, 3500000, "Active"),
            ("C02", "English Communication", "Intermediate communication", "Intermediate", 16, 4000000, "Active"),
            ("C03", "Cambridge Young Learners", "Cambridge prep for kids", "Beginner", 20, 4500000, "Active"),
            ("C04", "Cambridge Young Learners", "Cambridge intermediate", "Intermediate", 24, 5000000, "Active"),
            ("C05", "IELTS Preparation", "IELTS foundation", "Pre-IELTS", 16, 6000000, "Active"),
            ("C06", "IELTS Preparation", "Advanced IELTS prep", "Advanced", 20, 7000000, "Active"),
        ]
        cursor.executemany(
            "INSERT INTO Course (course_id, course_name, description, level, duration_weeks, tuition_fee, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            courses
        )

        # Seed skills
        skills = [
            ("SK01", "C01", "Listening", "Basic listening skills"),
            ("SK02", "C01", "Speaking", "Basic speaking skills"),
            ("SK03", "C02", "Listening", "Intermediate listening"),
            ("SK04", "C02", "Speaking", "Intermediate speaking"),
            ("SK05", "C05", "IELTS Listening", "IELTS listening practice"),
            ("SK06", "C05", "IELTS Reading", "IELTS reading practice"),
            ("SK07", "C05", "IELTS Writing", "IELTS writing practice"),
            ("SK08", "C05", "IELTS Speaking", "IELTS speaking practice"),
        ]
        cursor.executemany(
            "INSERT INTO Skill (skill_id, course_id, skill_name, description) VALUES (?, ?, ?, ?)",
            skills
        )

        # Seed teachers
        teachers = [
            ("T001", "Nguyen Van An", "0901000001", "an@school.com", "Listening & Speaking", "2020-01-15", "Active"),
            ("T002", "Tran Thi Bich", "0901000002", "bich@school.com", "Reading & Writing", "2020-03-20", "Active"),
            ("T003", "Le Van Cuong", "0901000003", "cuong@school.com", "IELTS", "2019-06-01", "Active"),
            ("T004", "Pham Thi Dung", "0901000004", "dung@school.com", "Cambridge", "2021-02-10", "Active"),
            ("T005", "Hoang Van Em", "0901000005", "em@school.com", "Listening & Speaking", "2022-01-05", "Active"),
            ("T006", "Vo Thi Phuong", "0901000006", "phuong@school.com", "Reading & Writing", "2018-09-12", "Active"),
            ("T007", "Nguyen Thi Giang", "0901000007", "giang@school.com", "IELTS", "2017-04-25", "Active"),
            ("T008", "Dang Van Hung", "0901000008", "hung@school.com", "Cambridge", "2023-01-01", "Active"),
        ]
        cursor.executemany(
            "INSERT INTO Teacher (teacher_id, full_name, phone_number, email, specialization, hire_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            teachers
        )

        # Seed rooms
        rooms = [
            ("R001", "Room 101", 20, "Building A - Floor 1", "Active"),
            ("R002", "Room 102", 15, "Building A - Floor 1", "Active"),
            ("R003", "Room 201", 25, "Building A - Floor 2", "Active"),
            ("R004", "Room 202", 20, "Building A - Floor 2", "Active"),
            ("R005", "Lab 301", 30, "Building B - Floor 3", "Active"),
        ]
        cursor.executemany(
            "INSERT INTO Room (room_id, room_name, capacity, location, status) VALUES (?, ?, ?, ?, ?)",
            rooms
        )

        # Seed classes
        classes = [
            ("L001", "English Beginner A1", "SK01", "T001", "2024-01-15", "2024-04-15", 20, "Active"),
            ("L002", "English Beginner A2", "SK02", "T002", "2024-02-01", "2024-05-01", 18, "Active"),
            ("L003", "IELTS Foundation", "SK05", "T003", "2024-03-01", "2024-06-30", 15, "Active"),
            ("L004", "IELTS Advanced", "SK06", "T007", "2024-01-20", "2024-05-20", 12, "Active"),
        ]
        cursor.executemany(
            "INSERT INTO Class (class_id, class_name, skill_id, teacher_id, start_date, end_date, max_student, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            classes
        )

        # Seed students (50 students)
        students = []
        for i in range(1, 51):
            students.append((
                f"S{i:03d}",
                f"Student {i:03d}",
                f"200{(i % 9) + 1}-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
                "Male" if i % 2 == 0 else "Female",
                f"Address {i}, Ho Chi Minh City",
                f"090{i:07d}",
                f"student{i:03d}@email.com",
                "2024-01-01",
                "Active"
            ))
        cursor.executemany(
            "INSERT INTO Student (student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            students
        )

        # Seed enrollments
        enrollments = [
            ("E001", "S001", "C01", "2024-01-10", "2024-01-15", "2024-04-15", "Active"),
            ("E002", "S002", "C01", "2024-01-10", "2024-01-15", "2024-04-15", "Active"),
            ("E003", "S003", "C05", "2024-02-20", "2024-03-01", "2024-06-30", "Active"),
            ("E004", "S004", "C05", "2024-02-25", "2024-03-01", "2024-06-30", "Active"),
            ("E005", "S005", "C02", "2024-01-25", "2024-02-01", "2024-05-01", "Active"),
        ]
        cursor.executemany(
            "INSERT INTO Enrollment (enrollment_id, student_id, course_id, enrollment_date, start_date, end_date, enrollment_status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            enrollments
        )

        # Seed class enrollments
        class_enrollments = [
            ("CE001", "L001", "E001", "2024-01-15"),
            ("CE002", "L001", "E002", "2024-01-15"),
            ("CE003", "L003", "E003", "2024-03-01"),
            ("CE004", "L003", "E004", "2024-03-01"),
            ("CE005", "L002", "E005", "2024-02-01"),
        ]
        cursor.executemany(
            "INSERT INTO Class_Enrollment (class_enrollment_id, class_id, enrollment_id, enroll_date) VALUES (?, ?, ?, ?)",
            class_enrollments
        )

        # Seed payments
        payments = [
            ("P001", "E001", "2024-01-10", 3500000, "Completed", "Full payment"),
            ("P002", "E002", "2024-01-10", 1750000, "Partial", "50% deposit"),
            ("P003", "E003", "2024-02-20", 6000000, "Completed", "Full payment"),
            ("P004", "E004", "2024-02-25", 3000000, "Partial", "50% deposit"),
            ("P005", "E005", "2024-01-25", 4000000, "Completed", "Full payment"),
        ]
        cursor.executemany(
            "INSERT INTO Payment (payment_id, enrollment_id, payment_date, amount, payment_status, note) VALUES (?, ?, ?, ?, ?, ?)",
            payments
        )

        conn.commit()
        print("Seed data inserted successfully!")
        
    except pyodbc.Error as e:
        print(f"Error inserting seed data: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    if test_connection():
        init_seed_data()
