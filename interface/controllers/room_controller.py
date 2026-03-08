from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout,
)
from PyQt6.QtCore import pyqtSignal, Qt

from interface.views.generated.room_ui import Ui_MainWindow
from infrastructure.repositories.room_repository import RoomRepository


class RoomController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_quaylai2.clicked.connect(self.go_back.emit)

        if hasattr(self.ui, "pushButton_dangxuat2"):
            self.ui.pushButton_dangxuat2.clicked.connect(self.handle_logout)

        self.ui.pushButton_them2.clicked.connect(self.handle_add)
        self.ui.pushButton_capnhat.clicked.connect(self.refresh)
        self.ui.pushButton_dongmo.clicked.connect(self.handle_toggle_status)

        self.load_data()

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def load_data(self):
        data = RoomRepository.get_all_rooms()
        self.ui.table_quanly2.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.table_quanly2.setItem(row_idx, col_idx, item)
        if hasattr(self.ui, "label_sophong"):
            self.ui.label_sophong.setText(str(len(data)))

    def show_input_form(self, title, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("""
            QDialog { background-color: white; border: 2px solid #bc1823; }
            QLabel { color: #bc1823; font-weight: bold; }
            QLineEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        self.inputs = {
            "id": QLineEdit(), "name": QLineEdit(),
            "cap": QLineEdit(), "type": QLineEdit(), "status": QLineEdit(),
        }
        if data:
            keys = list(self.inputs.keys())
            for i, key in enumerate(keys):
                self.inputs[key].setText(str(data[i]))
            self.inputs["id"].setReadOnly(True)
        labels = ["Room ID:", "Room Name:", "Capacity:", "Type:", "Status:"]
        for label, key in zip(labels, self.inputs):
            form_layout.addRow(label, self.inputs[key])
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [i.text() for i in self.inputs.values()]
        return None

    def handle_add(self):
        res = self.show_input_form("Add Room")
        if res:
            try:
                RoomRepository.insert_room(res)
                self.load_data()
                QMessageBox.information(self, "Success", "Room added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def refresh(self):
        self.load_data()
        QMessageBox.information(self, "Info", "Room list refreshed!")

    def handle_toggle_status(self):
        row = self.ui.table_quanly2.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a row first!")
            return
        room_id = self.ui.table_quanly2.item(row, 0).text()
        current_status = self.ui.table_quanly2.item(row, 4).text()
        new_status = "Inactive" if current_status == "Active" else "Active"
        try:
            RoomRepository.update_status(room_id, new_status)
            self.load_data()
            QMessageBox.information(self, "Success", f"Room {room_id} is now {new_status}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
