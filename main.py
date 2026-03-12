import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from interface.controllers.login_controller import LoginController
from interface.controllers.dashboard_controller import DashboardController
from interface.controllers.course_controller import CourseController
from interface.controllers.teacher_controller import TeacherController
from interface.controllers.room_controller import RoomController
from interface.controllers.user_controller import UserController
from interface.controllers.class_controller import ClassController
from interface.controllers.teacher.class_list_controller import TeacherClassListController


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("English Center Manager")
        self.current_user_ref_id = None  # Store logged-in user's ref_id

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login = LoginController()
        self.home = DashboardController()
        self.course = CourseController()
        self.teacher = TeacherController()
        self.room = RoomController()
        self.user = UserController()
        self.class_view = ClassController()
        self.teacher_view = TeacherClassListController()

        self.stack.addWidget(self.login)        # index 0
        self.stack.addWidget(self.home)         # index 1
        self.stack.addWidget(self.course)       # index 2
        self.stack.addWidget(self.teacher)      # index 3
        self.stack.addWidget(self.room)         # index 4
        self.stack.addWidget(self.user)         # index 5
        self.stack.addWidget(self.class_view)   # index 6
        self.stack.addWidget(self.teacher_view) # index 7

        self.connect_signals()
        self.stack.setCurrentWidget(self.login)

    def connect_signals(self):
        self.login.login_success.connect(self.route_by_role)

        self.home.go_to_teacher.connect(lambda: self.stack.setCurrentWidget(self.teacher))
        self.home.go_to_course.connect(lambda: self.stack.setCurrentWidget(self.course))
        self.home.go_to_room.connect(lambda: self.stack.setCurrentWidget(self.room))
        self.home.go_to_user.connect(lambda: self.stack.setCurrentWidget(self.user))
        self.home.logout_requested.connect(self.show_login)

        self.teacher.go_back.connect(self.back_home)
        self.teacher.logout_requested.connect(self.show_login)

        self.course.go_back.connect(self.back_home)
        self.course.logout_requested.connect(self.show_login)

        self.room.go_back.connect(self.back_home)
        self.room.logout_requested.connect(self.show_login)

        self.user.go_back.connect(self.back_home)
        self.user.logout_requested.connect(self.show_login)

        self.class_view.logout_requested.connect(self.show_login)
        self.teacher_view.logout_requested.connect(self.show_login)

    def route_by_role(self, role: str, ref_id: str):
        self.current_user_ref_id = ref_id
        if role == "admin":
            self.back_home()
        elif role == "staff":
            self.class_view.load_data()  # Refresh data when showing
            self.stack.setCurrentWidget(self.class_view)
        elif role == "teacher":
            self.teacher_view.set_teacher_id(ref_id)  # Set teacher filter
            self.stack.setCurrentWidget(self.teacher_view)
        else:
            self.back_home()

    def back_home(self):
        self.home.update_stats()  # Refresh statistics when returning to dashboard
        self.stack.setCurrentWidget(self.home)

    def show_login(self):
        self.current_user_ref_id = None
        self.stack.setCurrentWidget(self.login)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
