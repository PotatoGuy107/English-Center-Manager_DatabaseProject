from MODELS.student import Student
from PyQt6.QtCore import QDate


class FakeStudentRepository:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
                
            cls._instance.students = [

                Student(
                    "L001",                
                    "HV001",               
                    "Nguyễn Văn An",      
                    QDate(2005, 5, 12),     
                    "Nam",
                    "Hà Nội",
                    "0912345678",
                    "an@gmail.com",
                    QDate(2026, 1, 10)   
                ),

                Student(
                    "L001",
                    "HV002",
                    "Trần Thị Bình",
                    QDate(2004, 8, 25),
                    "Nữ",
                    "Đà Nẵng",
                    "0987654321",
                    "binh@gmail.com",
                    QDate(2026, 1, 15)
                ),
                Student (
                        "L002",
                        "HV003",
                        "Lê Văn C",
                        QDate(2006, 1, 5),
                        "Nam",
                        "TP.HCM",
                        "0909123456",
                        "c@gmail.com",
                        QDate.currentDate()
                    ),
            ]
            cls._instance.next_id = 4
        
        return cls._instance

    def get_students_by_class(self, class_code):
        return [
            s for s in self.students
            if s.class_code == class_code
        ]


    def search_students(self, keyword):

        keyword = keyword.strip().lower()


        return [
            s for s in self.students
            if keyword in s.student_id.lower()
            or keyword in s.name.lower()
        ]
    def update_student(self, student_id, name, phone, email):

            for s in self.students:
                if s.student_id == student_id:
                    s.name = name
                    s.phone = phone
                    s.email = email
                    return True

            return False
    #id dùng tạm lúc chưa tích hợp sql
    def add_student(self, student):
        self.students.append(student)
        self.next_id += 1
        
    def generate_student_id(self):
        max_id = 0

        for s in self.students:
            try:
                num = int(s.student_id.replace("HV", ""))
                if num > max_id:
                    max_id = num
            except:
                pass

        return f"HV{max_id + 1:03d}"
    def exists(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return True
        return False
    def delete_student(self, student_id):
        self.students = [
            s for s in self.students
            if s.student_id != student_id
        ]

