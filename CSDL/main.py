from PyQt6.QtWidgets import QApplication
from CONTROLL.controllclass import TaoLopController
import sys

app = QApplication(sys.argv)
window = TaoLopController()
window.show()
sys.exit(app.exec())
