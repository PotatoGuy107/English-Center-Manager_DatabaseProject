from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QComboBox
from PyQt6.QtCore import QDate, pyqtSignal, Qt
from PyQt6.QtGui import QBrush, QColor
from datetime import datetime

from interface.views.generated.class_management_ui import Ui_Dialog
from application.use_cases.class_use_cases import ClassUseCases
from application.use_cases.schedule_use_cases import ScheduleUseCases
from infrastructure.repositories.course_repository import CourseRepository
from infrastructure.repositories.skill_repository import SkillRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.room_repository import RoomRepository
from infrastructure.repositories.class_repository import ClassRepository


class ClassController(QDialog):
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.use_cases = ClassUseCases()
        self.schedule_use_cases = ScheduleUseCases()
        self.courses = []  # cache for courses
        self.skills = []   # cache for skills by course
        self.teachers = [] # cache for teachers
        self.rooms = []    # cache for rooms
        self.classes = []  # cache for classes
        self.current_class_id = None  # store created class for schedule
        self.selected_schedule_id = None  # store selected schedule for deletion
        
        self.apply_styles()
        self.connect_signals()
        self.load_data()
        
        # Show first tab (Tạo lớp)
        self.ui.tabWidget_2.setCurrentIndex(0)

    def apply_styles(self):
        """Apply custom styles to form elements"""
        # Expand form layout widget to fit all rows properly
        self.ui.formLayoutWidget_7.setGeometry(20, 20, 880, 350)
        self.ui.groupBox_6.setGeometry(20, 380, 880, 150)
        
        # Style for sidebar buttons - make them more visible
        sidebar_btn_style = """
            QPushButton {
                background-color: #bc1823;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #8b0000;
            }
        """
        self.ui.Button_taolop.setStyleSheet(sidebar_btn_style)
        self.ui.Button_dslop.setStyleSheet(sidebar_btn_style)
        self.ui.Button_logout.setStyleSheet(sidebar_btn_style)
        
        # Style for tab widget
        self.ui.tabWidget_2.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bc1823;
                border-radius: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #ffecee;
                color: #bc1823;
                font-weight: bold;
                padding: 10px 20px;
                border: 1px solid #bc1823;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #bc1823;
                color: white;
            }
        """)
        
        # Adjust form layout spacing
        self.ui.formLayout_7.setVerticalSpacing(20)
        self.ui.formLayout_7.setHorizontalSpacing(30)
        self.ui.formLayout_7.setContentsMargins(10, 10, 10, 10)
        
        self.ui.formLayout_8.setVerticalSpacing(20)
        self.ui.formLayout_8.setHorizontalSpacing(30)
        self.ui.formLayout_8.setContentsMargins(10, 10, 10, 10)
        
        # Style for form labels - darker color for visibility
        label_style = "color: #222; font-weight: bold; font-size: 13px; min-width: 150px;"
        for label in [self.ui.label_5, self.ui.label_22, self.ui.label_7, 
                      self.ui.label_19, self.ui.label_20, self.ui.label_21,
                      self.ui.label_23, self.ui.label_24]:
            label.setStyleSheet(label_style)
            label.setFixedHeight(40)
        
        # Style for combo boxes - fix dropdown text color
        combo_style = """
            QComboBox {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 13px;
                color: #222;
                min-height: 35px;
            }
            QComboBox:focus {
                border: 2px solid #8b0000;
                background-color: #ffe0e0;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #bc1823;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #222;
                selection-background-color: #bc1823;
                selection-color: white;
                border: 2px solid #bc1823;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                min-height: 30px;
                color: #222;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #ffecee;
                color: #bc1823;
            }
        """
        for combo in [self.ui.choosecourse_2, self.ui.chooseskill_2, self.ui.gvphutrach_2]:
            combo.setStyleSheet(combo_style)
            combo.setFixedHeight(40)
        
        # Style for line edits
        self.ui.nameclass_2.setStyleSheet("""
            QLineEdit {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 13px;
                color: #222;
                min-height: 35px;
            }
            QLineEdit:focus {
                border: 2px solid #8b0000;
                background-color: #ffe0e0;
            }
        """)
        self.ui.nameclass_2.setFixedHeight(40)
        
        # Style for info labels (thoi luong, hoc phi)
        info_label_style = "color: #bc1823; font-weight: bold; font-size: 14px;"
        self.ui.thoiluongkhoa_2.setStyleSheet(info_label_style)
        self.ui.thoiluongkhoa_2.setFixedHeight(40)
        self.ui.hocphi_2.setStyleSheet(info_label_style)
        self.ui.hocphi_2.setFixedHeight(40)
        
        # Style for date edits
        date_style = """
            QDateEdit {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 13px;
                color: #222;
                min-height: 35px;
            }
            QDateEdit:focus {
                border: 2px solid #8b0000;
            }
            QDateEdit::drop-down {
                border: none;
                width: 25px;
            }
        """
        self.ui.datestart_2.setStyleSheet(date_style)
        self.ui.datestart_2.setFixedHeight(40)
        self.ui.dateEnd_2.setStyleSheet(date_style)
        self.ui.dateEnd_2.setFixedHeight(40)

    def connect_signals(self):
        # Sidebar buttons
        self.ui.Button_taolop.clicked.connect(lambda: self.ui.tabWidget_2.setCurrentIndex(0))
        self.ui.Button_dslop.clicked.connect(self.open_class_list)
        self.ui.Button_logout.clicked.connect(self.logout_requested.emit)
        
        # Tab 1: General info
        self.ui.choosecourse_2.currentIndexChanged.connect(self.on_course_selected)
        self.ui.save.clicked.connect(self.save_class)
        
        # Tab 2: Schedule
        self.ui.save_2.clicked.connect(self.save_schedule)
        self.ui.delete_2.clicked.connect(self.delete_schedule)
        self.ui.tabWidget_2.currentChanged.connect(self.on_tab_changed)
        self.ui.qlytrunglich_2.cellClicked.connect(self.on_schedule_table_clicked)

    def load_data(self):
        """Load all reference data from database"""
        self.load_courses()
        self.load_teachers()
        self.load_rooms()
        self.setup_schedule_tab()

    def setup_schedule_tab(self):
        """Setup the schedule tab with proper data"""
        # Setup time slot combos
        time_slots = [
            "Ca 1 (07:00 - 10:00)",
            "Ca 2 (10:00 - 12:30)",
            "Ca 3 (13:30 - 16:00)",
            "Ca 4 (18:00 - 20:30)"
        ]
        for combo in [self.ui.ca1_2, self.ui.ca2_2]:
            combo.clear()
            for slot in time_slots:
                combo.addItem(slot)
        
        # Setup room combos from database with capacity info
        for combo in [self.ui.room1_2, self.ui.room1_3]:
            combo.clear()
            combo.addItem("---Chọn phòng---", None)
            for room in self.rooms:
                if room[4] == "available":
                    # Show room name with capacity: "Phòng A (30 chỗ)"
                    display_text = f"{room[1]} ({room[2]} chỗ)"
                    combo.addItem(display_text, room[0])  # display, room_id
        
        # Set default dates
        self.ui.dateca1_2.setDate(QDate.currentDate())
        self.ui.dateca2_2.setDate(QDate.currentDate())
        
        # Add class selection combo dynamically to max_class_2 position
        # max_class_2 will now be used as class selection
        self.ui.sLNgTIALabel_2.setText("Chọn lớp:")
        self.load_class_combo()
        
        # Connect room combos to show availability
        self.ui.room1_2.currentIndexChanged.connect(lambda: self.check_room_availability(1))
        self.ui.room1_3.currentIndexChanged.connect(lambda: self.check_room_availability(2))
        self.ui.dateca1_2.dateChanged.connect(lambda: self.check_room_availability(1))
        self.ui.dateca2_2.dateChanged.connect(lambda: self.check_room_availability(2))
        self.ui.ca1_2.currentIndexChanged.connect(lambda: self.check_room_availability(1))
        self.ui.ca2_2.currentIndexChanged.connect(lambda: self.check_room_availability(2))
        
        # Apply styling to schedule tab elements
        self.apply_schedule_tab_styles()

    def apply_schedule_tab_styles(self):
        """Apply styles to schedule tab elements"""
        combo_style = """
            QComboBox {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
                color: #222;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #222;
                selection-background-color: #bc1823;
                selection-color: white;
            }
        """
        for combo in [self.ui.ca1_2, self.ui.ca2_2, self.ui.room1_2, self.ui.room1_3]:
            combo.setStyleSheet(combo_style)
        
        # Style for date edits in schedule tab - make text visible
        date_style = """
            QDateEdit {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
                color: #222;
            }
            QDateEdit:focus {
                border: 2px solid #8b0000;
                background-color: #ffe0e0;
            }
            QDateEdit::drop-down {
                border: none;
                width: 25px;
            }
        """
        for date_edit in [self.ui.dateca1_2, self.ui.dateca2_2]:
            date_edit.setStyleSheet(date_style)
        
        # Style for labels in schedule tab
        label_style = "color: #222; font-weight: bold; font-size: 12px;"
        for label in [self.ui.label_25, self.ui.label_26, self.ui.label_27, self.ui.label_28,
                      self.ui.label_29, self.ui.label_30]:
            label.setStyleSheet(label_style)
        
        # Style max_class_2 QLineEdit (max students field)
        if hasattr(self.ui, 'max_class_2'):
            self.ui.max_class_2.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: #222;
                    border: 2px solid #bc1823;
                    border-radius: 5px;
                    padding: 6px 10px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 2px solid #8b0000;
                    background-color: #fff5f5;
                }
            """)
            self.ui.max_class_2.setPlaceholderText("VD: 30")

    def load_courses(self):
        """Load courses into combo box"""
        self.courses = CourseRepository.get_all_courses()
        self.ui.choosecourse_2.clear()
        self.ui.choosecourse_2.addItem("---Chọn khóa học---", None)
        for course in self.courses:
            # course: (course_id, course_name, description, level, duration_weeks, tuition_fee, status)
            self.ui.choosecourse_2.addItem(course[1], course[0])  # course_name, course_id

    def load_teachers(self):
        """Load teachers into combo box"""
        self.teachers = TeacherRepository.get_all()
        self.ui.gvphutrach_2.clear()
        self.ui.gvphutrach_2.addItem("---Chọn giảng viên---", None)
        for teacher in self.teachers:
            # teacher: (teacher_id, full_name, phone_number, email, specialization, hire_date, status)
            self.ui.gvphutrach_2.addItem(teacher[1], teacher[0])  # full_name, teacher_id

    def load_rooms(self):
        """Load rooms into combo boxes"""
        self.rooms = RoomRepository.get_all_rooms()
        for combo in [self.ui.room1_2, self.ui.room1_3]:
            combo.clear()
            combo.addItem("---Chọn phòng---", None)
            for room in self.rooms:
                # room: (room_id, room_name, capacity, location, status)
                if room[4] == "available":  # Only show available rooms
                    combo.addItem(room[1], room[0])  # room_name, room_id

    def load_class_combo(self):
        """Load all classes into combo for schedule assignment"""
        self.classes = ClassRepository.get_all_classes()
        
        # Convert to editable combo if not already
        from PyQt6.QtWidgets import QComboBox as QCB
        if not isinstance(self.ui.max_class_2, QCB):
            # Create a new combobox to replace the line edit
            combo = QCB(self.ui.formLayoutWidget_12)
            combo.setObjectName("class_select_combo")
            combo.setStyleSheet("""
                QComboBox {
                    background-color: white;
                    color: #222;
                    border: 2px solid #bc1823;
                    border-radius: 5px;
                    padding: 6px 10px;
                    font-size: 13px;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    color: #222;
                    selection-background-color: #bc1823;
                    selection-color: white;
                }
            """)
            # Replace in layout
            self.ui.formLayout_12.replaceWidget(self.ui.max_class_2, combo)
            self.ui.max_class_2.hide()
            self.ui.max_class_2 = combo
        
        self.ui.max_class_2.clear()
        self.ui.max_class_2.addItem("---Chọn lớp---", None)
        for cls in self.classes:
            # cls: (class_id, class_name, course_id, skill_id, teacher_id, ...)
            self.ui.max_class_2.addItem(f"{cls[0]} - {cls[1]}", cls[0])  # "ID - Name", class_id

    def check_room_availability(self, slot_num):
        """Check if room is available for the selected date/time and update UI"""
        if slot_num == 1:
            room_id = self.ui.room1_2.currentData()
            date = self.ui.dateca1_2.date().toPyDate()
            time_slot = self.ui.ca1_2.currentText()
            combo = self.ui.room1_2
        else:
            room_id = self.ui.room1_3.currentData()
            date = self.ui.dateca2_2.date().toPyDate()
            time_slot = self.ui.ca2_2.currentText()
            combo = self.ui.room1_3
        
        if not room_id:
            return
        
        # Parse time slot
        start_time, end_time = self.schedule_use_cases.parse_time_slot(time_slot)
        
        # Check conflict
        from infrastructure.repositories.schedule_repository import ScheduleRepository
        has_conflict, conflict_class = ScheduleRepository.check_room_conflict(
            room_id, date, start_time, end_time
        )
        
        if has_conflict:
            combo.setStyleSheet("""
                QComboBox {
                    background-color: #ffcccc;
                    color: #8b0000;
                    border: 2px solid red;
                    border-radius: 5px;
                    padding: 6px 10px;
                }
            """)
            combo.setToolTip(f"⚠ Phòng đã được sử dụng bởi: {conflict_class}")
        else:
            combo.setStyleSheet("""
                QComboBox {
                    background-color: #ccffcc;
                    color: #006400;
                    border: 2px solid green;
                    border-radius: 5px;
                    padding: 6px 10px;
                }
            """)
            combo.setToolTip("✓ Phòng trống")

    def on_course_selected(self, index):
        """Handle course selection to load skills and display course info"""
        course_id = self.ui.choosecourse_2.currentData()
        
        # Clear skill combo
        self.ui.chooseskill_2.clear()
        self.ui.chooseskill_2.addItem("---Chọn kỹ năng---", None)
        
        # Clear info labels
        self.ui.thoiluongkhoa_2.setText("")
        self.ui.hocphi_2.setText("")
        
        if course_id is None:
            return
        
        # Load course info
        course = CourseRepository.get_by_id(course_id)
        if course:
            # course: (course_id, course_name, description, level, duration_weeks, tuition_fee, status)
            self.ui.thoiluongkhoa_2.setText(f"{course[4]} tuần")
            self.ui.hocphi_2.setText(f"{course[5]:,.0f} VNĐ")
        
        # Load skills for selected course
        self.skills = SkillRepository.get_by_course(course_id)
        for skill in self.skills:
            # skill: (skill_id, skill_name, description)
            self.ui.chooseskill_2.addItem(skill[1], skill[0])  # skill_name, skill_id

    def save_class(self):
        """Save class from form data"""
        # Validate required fields
        course_id = self.ui.choosecourse_2.currentData()
        skill_id = self.ui.chooseskill_2.currentData()
        teacher_id = self.ui.gvphutrach_2.currentData()
        class_name = self.ui.nameclass_2.text().strip()
        start_date = self.ui.datestart_2.date()
        end_date = self.ui.dateEnd_2.date()
        
        if not course_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khóa học!")
            return
        if not skill_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn kỹ năng!")
            return
        if not teacher_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giảng viên!")
            return
        if not class_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên lớp!")
            return
        if start_date > end_date:
            QMessageBox.warning(self, "Lỗi", "Ngày bắt đầu phải trước ngày kết thúc!")
            return
        
        data = {
            "name": class_name,
            "course": self.ui.choosecourse_2.currentText(),
            "skill": skill_id,
            "teacher": teacher_id,
            "start_date": start_date,
            "end_date": end_date,
            "max_students": 25,
            "status": "planned"
        }
        
        success, result = self.use_cases.create_class(data)
        if success:
            try:
                self.current_class_id = int(result)  # Store class_id for schedule tab
            except (ValueError, TypeError):
                self.current_class_id = result
            QMessageBox.information(self, "Thành công", 
                f"Đã tạo lớp (ID: {result})\nChuyển sang tab 'Xếp thời khóa biểu' để thêm lịch học")
            self.clear_form()
            try:
                self.load_schedule_table()  # Refresh schedule table
            except Exception as e:
                pass  # Don't crash, just skip refresh
        else:
            QMessageBox.warning(self, "Lỗi", result)

    def clear_form(self):
        """Clear all form fields"""
        self.ui.choosecourse_2.setCurrentIndex(0)
        self.ui.chooseskill_2.setCurrentIndex(0)
        self.ui.gvphutrach_2.setCurrentIndex(0)
        self.ui.nameclass_2.clear()
        self.ui.datestart_2.setDate(QDate.currentDate())
        self.ui.dateEnd_2.setDate(QDate.currentDate().addMonths(3))

    def on_tab_changed(self, index):
        """Handle tab change event"""
        if index == 1:  # Schedule tab
            try:
                self.load_schedule_table()
                self.load_class_combo()  # Refresh class list
            except Exception as e:
                import traceback
                QMessageBox.critical(self, "Lỗi", f"Lỗi load lịch học:\n{str(e)}")

    def load_schedule_table(self):
        """Load all schedules into the table"""
        try:
            schedules = self.schedule_use_cases.get_all_schedules()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi truy vấn lịch học:\n{str(e)}")
            schedules = []
        
        # Setup table
        self.ui.qlytrunglich_2.setAlternatingRowColors(False)
        self.ui.qlytrunglich_2.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        self.ui.qlytrunglich_2.setRowCount(len(schedules))
        
        for row, schedule in enumerate(schedules):
            # schedule: (schedule_id, class_id, class_name, room_id, room_name,
            #            teacher_name, max_student, study_date, time_slot, start_time, end_time, status)
            
            # STT
            item = QTableWidgetItem(str(row + 1))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 0, item)
            
            # Mã lớp (class_id)
            item = QTableWidgetItem(str(schedule[1]))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 1, item)
            
            # Giảng viên
            item = QTableWidgetItem(str(schedule[5] or ""))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 2, item)
            
            # Sĩ số
            item = QTableWidgetItem(str(schedule[6] or ""))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 3, item)
            
            # Ngày
            study_date = schedule[7]
            if study_date:
                date_str = study_date.strftime("%d/%m/%Y")
            else:
                date_str = ""
            item = QTableWidgetItem(date_str)
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 4, item)
            
            # Ca
            item = QTableWidgetItem(str(schedule[8] or ""))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 5, item)
            
            # Phòng
            item = QTableWidgetItem(str(schedule[4] or ""))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 6, item)
            
            # Trạng thái
            item = QTableWidgetItem(str(schedule[11] or ""))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.qlytrunglich_2.setItem(row, 7, item)
            
            # Store schedule_id in first column's data
            first_item = self.ui.qlytrunglich_2.item(row, 0)
            if first_item:
                first_item.setData(Qt.ItemDataRole.UserRole, schedule[0])  # schedule_id

    def on_schedule_table_clicked(self, row, column):
        """Handle table row click to select schedule for deletion"""
        item = self.ui.qlytrunglich_2.item(row, 0)
        if item:
            self.selected_schedule_id = item.data(Qt.ItemDataRole.UserRole)

    def save_schedule(self):
        """Save schedule from form data"""
        # Get class from combo
        class_id = self.ui.max_class_2.currentData() if hasattr(self.ui.max_class_2, 'currentData') else None
        
        # Fallback to current_class_id if combo doesn't have selection
        if not class_id:
            class_id = self.current_class_id
        
        if not class_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp học!")
            return
        
        # Get schedule 1 data
        date1 = self.ui.dateca1_2.date().toPyDate()
        time_slot1 = self.ui.ca1_2.currentText()
        room_id1 = self.ui.room1_2.currentData()
        
        # Get schedule 2 data (optional)
        date2 = self.ui.dateca2_2.date().toPyDate()
        time_slot2 = self.ui.ca2_2.currentText()
        room_id2 = self.ui.room1_3.currentData()
        
        added_count = 0
        errors = []
        
        # Add schedule 1
        if room_id1:
            success, msg = self.schedule_use_cases.add_schedule(
                class_id, room_id1, date1, time_slot1
            )
            if success:
                added_count += 1
            else:
                errors.append(f"Ca 1: {msg}")
        
        # Add schedule 2 if room selected
        if room_id2:
            success, msg = self.schedule_use_cases.add_schedule(
                class_id, room_id2, date2, time_slot2
            )
            if success:
                added_count += 1
            else:
                errors.append(f"Ca 2: {msg}")
        
        # Show result
        if added_count > 0:
            result_msg = f"Đã thêm {added_count} buổi học"
            if errors:
                result_msg += f"\n\nLỗi:\n" + "\n".join(errors)
            QMessageBox.information(self, "Thành công", result_msg)
            self.load_schedule_table()
            self.current_class_id = None  # Reset after successful add
            # Reset room combo styles
            self.reset_room_combo_styles()
        elif errors:
            QMessageBox.warning(self, "Lỗi", "\n".join(errors))
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn phòng học!")

    def reset_room_combo_styles(self):
        """Reset room combo box styles to default"""
        default_style = """
            QComboBox {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
                color: #222;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #222;
                selection-background-color: #bc1823;
                selection-color: white;
            }
        """
        self.ui.room1_2.setStyleSheet(default_style)
        self.ui.room1_3.setStyleSheet(default_style)
        self.ui.room1_2.setToolTip("")
        self.ui.room1_3.setToolTip("")

    def delete_schedule(self):
        """Delete selected schedule"""
        if not self.selected_schedule_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lịch cần xóa từ bảng!")
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Xác nhận", 
            f"Bạn có chắc muốn xóa lịch học này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.schedule_use_cases.delete_schedule(self.selected_schedule_id)
            if success:
                QMessageBox.information(self, "Thành công", msg)
                self.load_schedule_table()
                self.selected_schedule_id = None
            else:
                QMessageBox.warning(self, "Lỗi", msg)

    def open_class_list(self):
        """Open class list window"""
        from interface.controllers.class_list_controller import ClassListController
        self.class_list_window = ClassListController()
        self.class_list_window.show()
