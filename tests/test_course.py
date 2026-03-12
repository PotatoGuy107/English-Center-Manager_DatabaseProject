import unittest
from src.models.course import Course
from src.bll.course_bll import CourseBLL

class TestCourse(unittest.TestCase):

    def setUp(self):
        self.course_bll = CourseBLL()
        self.course = Course(course_id=1, name="Mathematics", description="Basic Math Course")

    def test_create_course(self):
        result = self.course_bll.create_course(self.course)
        self.assertTrue(result)

    def test_get_course(self):
        self.course_bll.create_course(self.course)
        retrieved_course = self.course_bll.get_course(self.course.course_id)
        self.assertEqual(retrieved_course.name, self.course.name)

    def test_update_course(self):
        self.course_bll.create_course(self.course)
        self.course.name = "Advanced Mathematics"
        result = self.course_bll.update_course(self.course)
        self.assertTrue(result)
        updated_course = self.course_bll.get_course(self.course.course_id)
        self.assertEqual(updated_course.name, "Advanced Mathematics")

    def test_delete_course(self):
        self.course_bll.create_course(self.course)
        result = self.course_bll.delete_course(self.course.course_id)
        self.assertTrue(result)
        deleted_course = self.course_bll.get_course(self.course.course_id)
        self.assertIsNone(deleted_course)

if __name__ == '__main__':
    unittest.main()