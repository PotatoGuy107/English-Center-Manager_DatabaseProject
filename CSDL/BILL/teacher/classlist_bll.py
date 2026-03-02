from DAL.class_dal import ClassDAL


class ClasslistBLL:
    def __init__(self):
        self.repo = ClassDAL()

    def get_all_classes(self):
        # Ở đây có thể thêm business rule
        classes = self.repo.get_all_classes()

        # Ví dụ rule:
        # chỉ lấy lớp còn hoạt động
        # classes = [c for c in classes if c.is_active]

        return classes
