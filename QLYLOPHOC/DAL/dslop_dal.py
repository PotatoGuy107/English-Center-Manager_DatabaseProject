class FakeClassRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Fake data ban đầu
            cls._instance.classes = [
                ("L001", "Speaking", "Nguyễn Minh Anh",
                 "01/05/2026", "30/06/2026", "25/25", "Đang học"),

                ("L002", "Listening", "Trần Thu Hà",
                 "05/05/2026", "05/07/2026", "20/50", "Sắp khai giảng"),
            ]

        return cls._instance

    # lấy danh sách lớp
    def get_all_classes(self):
        return self.classes

    # thêm lớp mới
    def add_class(self, class_data):
        self.classes.append(class_data)
