import unittest
from src.models.teacher import Teacher
from src.dal.teacher_dal import TeacherDAL

class TestTeacher(unittest.TestCase):

    def setUp(self):
        self.teacher_dal = TeacherDAL()
        self.teacher = Teacher(name="John Doe", subject="Mathematics")

    def test_create_teacher(self):
        result = self.teacher_dal.create_teacher(self.teacher)
        self.assertTrue(result)

    def test_get_teacher(self):
        self.teacher_dal.create_teacher(self.teacher)
        retrieved_teacher = self.teacher_dal.get_teacher(self.teacher.id)
        self.assertEqual(retrieved_teacher.name, self.teacher.name)

    def test_update_teacher(self):
        self.teacher_dal.create_teacher(self.teacher)
        self.teacher.name = "Jane Doe"
        result = self.teacher_dal.update_teacher(self.teacher)
        self.assertTrue(result)

    def test_delete_teacher(self):
        self.teacher_dal.create_teacher(self.teacher)
        result = self.teacher_dal.delete_teacher(self.teacher.id)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()