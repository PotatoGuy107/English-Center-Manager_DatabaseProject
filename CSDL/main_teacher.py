import sys
from PyQt6.QtWidgets import QApplication
from CONTROLL.teacher.classlist_controll import TeacherClassList

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TeacherClassList()
    window.show()

    sys.exit(app.exec())
