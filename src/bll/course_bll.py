class CourseBLL:
    def __init__(self, course_dal):
        self.course_dal = course_dal

    def get_all_courses(self):
        return self.course_dal.get_all_courses()

    def get_course_by_id(self, course_id):
        return self.course_dal.get_course_by_id(course_id)

    def add_course(self, course):
        return self.course_dal.add_course(course)

    def update_course(self, course):
        return self.course_dal.update_course(course)

    def delete_course(self, course_id):
        return self.course_dal.delete_course(course_id)