from PyQt6.QtCore import pyqtSignal, QObject
from ..bll.teacher_bll import TeacherBLL

class TeacherController(QObject):
    teacher_added = pyqtSignal()
    teacher_updated = pyqtSignal()
    teacher_deleted = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.teacher_bll = TeacherBLL()

    def add_teacher(self, teacher_data):
        success = self.teacher_bll.add_teacher(teacher_data)
        if success:
            self.teacher_added.emit()

    def update_teacher(self, teacher_id, teacher_data):
        success = self.teacher_bll.update_teacher(teacher_id, teacher_data)
        if success:
            self.teacher_updated.emit()

    def delete_teacher(self, teacher_id):
        success = self.teacher_bll.delete_teacher(teacher_id)
        if success:
            self.teacher_deleted.emit()

    def get_teachers(self):
        return self.teacher_bll.get_all_teachers()