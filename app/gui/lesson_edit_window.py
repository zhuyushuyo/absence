from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QComboBox, QDateEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QDate
from ..database.db_manager import DatabaseManager

class LessonEditWindow(QMainWindow):
    def __init__(self, lesson_data, db_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Lesson Info")
        self.setGeometry(200, 200, 400, 400)
        self.parent = parent
        self.db_manager = db_manager
        self.lesson_data = lesson_data

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.lesson_edit = QLineEdit()
        self.lesson_edit.setText(lesson_data.get("name", ""))
        self.lesson_edit.setPlaceholderText("Lesson Name")
        layout.addWidget(self.lesson_edit)

        self.day_combo = QComboBox()
        self.day_combo.addItems(["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"])
        self.day_combo.setCurrentText(lesson_data.get("day", "月曜日"))
        layout.addWidget(self.day_combo)

        self.period_edit = QLineEdit()
        self.period_edit.setText(lesson_data.get("period", ""))
        self.period_edit.setPlaceholderText("時限 (e.g., 1-2)")
        layout.addWidget(self.period_edit)

        self.begin_date_edit = QDateEdit()
        self.begin_date_edit.setDate(lesson_data.get("begin_date", QDate.currentDate()))
        self.begin_date_edit.setCalendarPopup(True)
        self.begin_date_edit.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.begin_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(lesson_data.get("end_date", QDate.currentDate()))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.end_date_edit)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

    def save_changes(self):
        try:
            lesson_name = self.lesson_edit.text()
            if not lesson_name:
                QMessageBox.warning(self, "Missing Input", "Please enter a lesson name.")
                return

            begin_date = self.begin_date_edit.date()
            end_date = self.end_date_edit.date()
            if begin_date > end_date:
                QMessageBox.warning(self, "Invalid Dates", "Begin date must be before or equal to end date.")
                return

            updated_data = {
                "name": lesson_name,
                "day": self.day_combo.currentText(),
                "period": self.period_edit.text() or "N/A",
                "begin_date": begin_date,
                "end_date": end_date
            }

            if self.parent:
                self.parent.update_lesson_data(self.lesson_data.get("name", ""), updated_data)
            QMessageBox.information(self, "Success", "Lesson info saved.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {str(e)}")