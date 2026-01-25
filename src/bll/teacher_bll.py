from dal.teacher_dal import TeacherDAL

class TeacherBLL:
    def __init__(self):
        self.teacher_dal = TeacherDAL()

    def add_teacher(self, teacher_data):
        return self.teacher_dal.insert_teacher(teacher_data)

    def get_teacher(self, teacher_id):
        return self.teacher_dal.fetch_teacher(teacher_id)

    def update_teacher(self, teacher_id, teacher_data):
        return self.teacher_dal.update_teacher(teacher_id, teacher_data)

    def delete_teacher(self, teacher_id):
        return self.teacher_dal.delete_teacher(teacher_id)

    def get_all_teachers(self):
        return self.teacher_dal.fetch_all_teachers()