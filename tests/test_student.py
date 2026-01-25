import unittest
from src.models.student import Student
from src.dal.student_dal import StudentDAL

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student_dal = StudentDAL()
        self.test_student = Student(name="John Doe", age=20, email="john.doe@example.com")

    def test_create_student(self):
        result = self.student_dal.create_student(self.test_student)
        self.assertTrue(result)

    def test_get_student(self):
        self.student_dal.create_student(self.test_student)
        student = self.student_dal.get_student(self.test_student.email)
        self.assertEqual(student.name, self.test_student.name)

    def test_update_student(self):
        self.student_dal.create_student(self.test_student)
        self.test_student.name = "Jane Doe"
        result = self.student_dal.update_student(self.test_student)
        self.assertTrue(result)

    def test_delete_student(self):
        self.student_dal.create_student(self.test_student)
        result = self.student_dal.delete_student(self.test_student.email)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()