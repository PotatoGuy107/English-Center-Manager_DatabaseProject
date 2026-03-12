from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout, QComboBox,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QBrush, QColor

from interface.views.generated.room_ui import Ui_MainWindow
from infrastructure.repositories.room_repository import RoomRepository

# Valid status values for Room table (CHECK constraint)
ROOM_STATUS_OPTIONS = ["available", "maintenance", "unavailable"]


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
        self.ui.table_quanly2.setAlternatingRowColors(False)
        self.ui.table_quanly2.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        self.ui.table_quanly2.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QBrush(QColor("#222")))
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
            QComboBox { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Create input fields
        self.inputs = {
            "id": QLineEdit(),
            "name": QLineEdit(),
            "cap": QLineEdit(),
            "location": QLineEdit(),
        }
        # Status is a dropdown with valid options
        self.status_combo = QComboBox()
        self.status_combo.addItems(ROOM_STATUS_OPTIONS)
        
        if data:
            self.inputs["id"].setText(str(data[0]))
            self.inputs["name"].setText(str(data[1]))
            self.inputs["cap"].setText(str(data[2]))
            self.inputs["location"].setText(str(data[3]))
            # Set current status in combo
            status_idx = self.status_combo.findText(str(data[4]))
            if status_idx >= 0:
                self.status_combo.setCurrentIndex(status_idx)
            self.inputs["id"].setReadOnly(True)
        else:
            # Adding new room - ID is auto-generated
            self.inputs["id"].setText("(Auto)")
            self.inputs["id"].setReadOnly(True)
        
        form_layout.addRow("Room ID:", self.inputs["id"])
        form_layout.addRow("Room Name:", self.inputs["name"])
        form_layout.addRow("Capacity:", self.inputs["cap"])
        form_layout.addRow("Location:", self.inputs["location"])
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [
                self.inputs["id"].text(),
                self.inputs["name"].text(),
                self.inputs["cap"].text(),
                self.inputs["location"].text(),
                self.status_combo.currentText()
            ]
        return None

    def handle_add(self):
        res = self.show_input_form("Add Room")
        if res:
            try:
                # data = (room_name, capacity, location, status) - room_id is auto-generated
                room_data = (res[1], res[2], res[3], res[4])
                new_room_id = RoomRepository.insert_room(room_data)
                self.load_data()
                QMessageBox.information(self, "Success", f"Room {new_room_id} added successfully!")
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
        # Toggle between available and unavailable
        new_status = "unavailable" if current_status == "available" else "available"
        try:
            RoomRepository.update_status(room_id, new_status)
            self.load_data()
            QMessageBox.information(self, "Success", f"Room {room_id} is now {new_status}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
