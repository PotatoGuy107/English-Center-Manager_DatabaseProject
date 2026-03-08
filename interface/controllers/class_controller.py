from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate, pyqtSignal

from interface.views.generated.class_management_ui import Ui_Dialog
from application.use_cases.class_use_cases import ClassUseCases
from domain.entities.schedule_entity import Schedule


class ClassController(QDialog):
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.use_cases = ClassUseCases()
        self.connect_signals()
        self.init_table()

    def connect_signals(self):
        if hasattr(self.ui, "Button_return"):
            self.ui.Button_return.clicked.connect(self.logout_requested.emit)
        if hasattr(self.ui, "btnluulop"):
            self.ui.btnluulop.clicked.connect(self.save_class)
        if hasattr(self.ui, "btnthemlịch"):
            self.ui.btnthemlịch.clicked.connect(self.add_schedule)
        if hasattr(self.ui, "btnxoalich"):
            self.ui.btnxoalich.clicked.connect(self.delete_schedule)
        if hasattr(self.ui, "btndslop"):
            self.ui.btndslop.clicked.connect(self.open_class_list)

    def open_class_list(self):
        from interface.controllers.class_list_controller import ClassListController
        self.class_list_window = ClassListController()
        self.class_list_window.show()

    def init_table(self):
        if hasattr(self.ui, "qlytrunglich_2"):
            self.ui.qlytrunglich_2.setRowCount(0)

    def add_schedule(self):
        pass

    def delete_schedule(self):
        pass

    def save_class(self):
        data = self._collect_form_data()
        if not data:
            return
        success, result = self.use_cases.create_class(data)
        if success:
            QMessageBox.information(self, "Success", f"Class created: {result}")
        else:
            QMessageBox.warning(self, "Error", result)

    def _collect_form_data(self):
        data = {}
        if hasattr(self.ui, "tenlop"):
            data["name"] = self.ui.tenlop.text().strip()
        if hasattr(self.ui, "combo_khoahoc"):
            data["course"] = self.ui.combo_khoahoc.currentText()
        if hasattr(self.ui, "combo_kynan"):
            data["skill"] = self.ui.combo_kynan.currentText()
        if hasattr(self.ui, "combo_gv"):
            data["teacher"] = self.ui.combo_gv.currentText()
        if hasattr(self.ui, "ngaybatdau"):
            data["start_date"] = self.ui.ngaybatdau.date()
        if hasattr(self.ui, "ngayketthuc"):
            data["end_date"] = self.ui.ngayketthuc.date()
        if hasattr(self.ui, "sisotoida"):
            try:
                data["max_students"] = int(self.ui.sisotoida.value())
            except Exception:
                data["max_students"] = 20
        return data
