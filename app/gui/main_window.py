import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QTextEdit, QMenuBar, QMessageBox, QFileDialog, \
    QInputDialog
from PyQt6.QtCore import QDate
import pandas as pd
from ..config.config_manager import ConfigManager
from ..database.db_manager import DatabaseManager
from .records_window import RecordsWindow
from .lesson_edit_window import LessonEditWindow
from .students_edit_window import StudentsEditWindow
from .submission_window import SubmissionWindow
from .import_details_window import ImportDetailsWindow


class AbsenceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Absence Confirmation Tool")
        self.setGeometry(100, 100, 600, 400)

        self.save_dir = os.path.join(os.getcwd(), "saving_data")
        os.makedirs(self.save_dir, exist_ok=True)

        self.config_manager = ConfigManager(os.path.join(self.save_dir, "config.json"))
        self.db_manager = DatabaseManager(os.path.join(self.save_dir, "submission_records.db"))

        self.student_ids = [
            "NUS:022500203", "NUS:022500410", "NUS:022500445", "NUS:032500107",
            "NUS:032500121", "NUS:042500444", "NUS:042500832", "NUS:042501247",
            "NUS:062300424", "NUS:062500293", "NUS:062500383", "NUS:062500408",
            "NUS:062501011", "NUS:7125W4015"
        ]

        self.lessons = self.db_manager.load_lessons()
        self.present_students = set()
        self.current_lesson = None

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.setup_menu_bar()

        self.lesson_combo = QComboBox()
        self.update_lesson_combo()
        self.lesson_combo.currentTextChanged.connect(self.update_lesson_info_display)
        layout.addWidget(self.lesson_combo)

        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setFixedHeight(100)
        layout.addWidget(self.info_display)

    def setup_menu_bar(self):
        try:
            menu_bar = self.menuBar()

            file_menu = menu_bar.addMenu("File")
            export_action = file_menu.addAction("Export")
            export_action.triggered.connect(self.export_to_excel)
            import_action = file_menu.addAction("Import")
            import_action.triggered.connect(self.import_data)
            setting_action = file_menu.addAction("Setting")
            setting_action.triggered.connect(
                lambda: QMessageBox.information(self, "Setting", "Settings not implemented."))

            edit_menu = menu_bar.addMenu("Edit")
            lesson_info_action = edit_menu.addAction("Edit Lesson Info")
            lesson_info_action.triggered.connect(self.open_lesson_edit)
            students_info_action = edit_menu.addAction("Edit Students Info")
            students_info_action.triggered.connect(self.open_students_edit)

            submission_menu = menu_bar.addMenu("Submission")
            submission_action = submission_menu.addAction("Open Submission Window")
            submission_action.triggered.connect(self.open_submission_window)

            view_menu = menu_bar.addMenu("View")
            records_action = view_menu.addAction("View Records")
            records_action.triggered.connect(self.view_records)

            help_menu = menu_bar.addMenu("Help")
            about_action = help_menu.addAction("About")
            about_action.triggered.connect(self.show_about)
            requirements_action = help_menu.addAction("Requirements")
            requirements_action.triggered.connect(self.show_requirements)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup menu bar: {str(e)}")

    def show_about(self):
        try:
            QMessageBox.information(self, "About",
                                    f"Absence Confirmation Tool\nVersion: {self.config_manager.get_version()}\nDeveloper: {self.config_manager.get_developer()}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show about info: {str(e)}")

    def show_requirements(self):
        try:
            requirements = "Required Libraries:\n- PyQt6\n- pandas\n- sqlite3 (built-in)\n- json (built-in)"
            QMessageBox.information(self, "Requirements", requirements)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show requirements: {str(e)}")

    def update_lesson_combo(self):
        try:
            self.lesson_combo.clear()
            self.lesson_combo.addItem("Select a Lesson")
            for lesson_name in self.lessons.keys():
                self.lesson_combo.addItem(lesson_name)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update lesson combo: {str(e)}")

    def update_lesson_info_display(self):
        try:
            lesson_name = self.lesson_combo.currentText()
            if lesson_name == "Select a Lesson" or not lesson_name:
                self.info_display.setText("")
                self.current_lesson = None
                return

            self.current_lesson = lesson_name
            lesson_data = self.lessons.get(lesson_name, {})
            student_count = len(self.student_ids)
            display_text = (f"Lesson: {lesson_data.get('name', '')}\n"
                            f"Day: {lesson_data.get('day', '')}\n"
                            f"Period: {lesson_data.get('period', '')}\n"
                            f"Students: {student_count}")
            self.info_display.setText(display_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update lesson info display: {str(e)}")

    def open_lesson_edit(self):
        try:
            lesson_name = self.lesson_combo.currentText()
            lesson_data = self.lessons.get(lesson_name, {"name": "", "day": "月曜日", "period": "",
                                                         "begin_date": QDate.currentDate(),
                                                         "end_date": QDate.currentDate()})
            lesson_window = LessonEditWindow(lesson_data, self.db_manager, self)
            lesson_window.show()
            self.lesson_window = lesson_window
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open lesson edit window: {str(e)}")

    def open_students_edit(self):
        try:
            students_window = StudentsEditWindow(self.student_ids, self)
            students_window.show()
            self.students_window = students_window
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open students edit window: {str(e)}")

    def open_submission_window(self):
        try:
            lesson_name = self.lesson_combo.currentText()
            if lesson_name == "Select a Lesson" or not lesson_name:
                QMessageBox.warning(self, "No Lesson Selected", "Please select a lesson first.")
                return
            lesson_data = self.lessons.get(lesson_name, {"name": "", "day": "月曜日", "period": "",
                                                         "begin_date": QDate.currentDate(),
                                                         "end_date": QDate.currentDate()})
            submission_window = SubmissionWindow(self.student_ids, lesson_data, self.present_students, self.db_manager,
                                                 self)
            submission_window.show()
            self.submission_window = submission_window
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open submission window: {str(e)}")

    def view_records(self):
        try:
            records = self.db_manager.fetch_records()
            if not records:
                QMessageBox.information(self, "No Records", "No submission records found.")
                return

            submissions = {}
            for record in records:
                date, lesson, day, period, student_id, status = record
                key = (date, lesson, day, period)
                if key not in submissions:
                    submissions[key] = {"present": [], "absent": []}
                if status == "Present":
                    submissions[key]["present"].append(student_id)
                else:
                    submissions[key]["absent"].append(student_id)

            summary_text = []
            absence_details = {}
            for key, data in submissions.items():
                date, lesson, day, period = key
                absence_count = len(data["absent"])
                absence_details[key] = data["absent"]
                if absence_count == 0:
                    summary_text.append(f"Date: {date}, Lesson: {lesson}, Day: {day}, Period: {period}, Full Presence")
                else:
                    summary_text.append(
                        f"Date: {date}, Lesson: {lesson}, Day: {day}, Period: {period}, {absence_count} absence(s)")

            records_window = RecordsWindow("\n".join(summary_text), absence_details, self)
            records_window.show()
            self.records_window = records_window
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to view records: {str(e)}")

    def export_to_excel(self):
        try:
            records = self.db_manager.fetch_submissions_for_export()
            if not records:
                QMessageBox.information(self, "No Records", "No submission records to export.")
                return

            df = pd.DataFrame(records, columns=["Date", "Lesson", "Day", "Period", "Student ID", "Status"])
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", self.save_dir, "Excel Files (*.xlsx)")
            if save_path:
                try:
                    df.to_excel(save_path, index=False)
                    QMessageBox.information(self, "Success", f"Submission records exported to {save_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export to Excel: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export to Excel: {str(e)}")

    def import_data(self):
        try:
            # Choose file type
            file_type, ok = QInputDialog.getItem(self, "Select File Type", "Choose the file type to import:",
                                                 ["SQLite Database (.db)", "Excel (.xlsx)"], 0, False)
            if not ok:
                return

            # Choose import type
            import_type, ok = QInputDialog.getItem(self, "Select Import Type", "Choose what to import:",
                                                   ["Lesson Info", "Student Info", "Presence Info"], 0, False)
            if not ok:
                return

            # Define required columns and details
            if import_type == "Lesson Info":
                required_columns = "name (unique text), day (e.g., 月曜日), period (e.g., 1-2), begin_date (yyyy-MM-dd), end_date (yyyy-MM-dd)"
                details_key = "lesson_info"
            elif import_type == "Student Info":
                required_columns = "student_id (unique text, e.g., NUS:022500203)"
                details_key = "student_info"
            else:  # Presence Info
                required_columns = "date (yyyy-MM-dd), lesson (text), day (e.g., 月曜日), period (e.g., 1-2), student_id (text), status (Present or Absent)"
                details_key = "presence_info"

            # Show required columns with "For more details" button
            msg = QMessageBox(self)
            msg.setWindowTitle("Import Requirements")
            msg.setText(f"Ensure the import file contains the following columns:\n{required_columns}")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            details_button = msg.addButton("For more details", QMessageBox.ButtonRole.ActionRole)
            result = msg.exec()

            if result == QMessageBox.StandardButton.Cancel:
                return
            elif msg.clickedButton() == details_button:
                details_window = ImportDetailsWindow(details_key, self)
                details_window.show()
                return  # Wait for user to proceed after viewing details

            # Select file
            if file_type == "SQLite Database (.db)":
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Database File", self.save_dir,
                                                           "SQLite Database (*.db)")
            else:  # Excel
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", self.save_dir,
                                                           "Excel Files (*.xlsx)")

            if not file_path:
                return

            # Import data
            success = False
            if import_type == "Lesson Info":
                success = self.db_manager.import_lesson_info(file_path, file_type == "SQLite Database (.db)")
            elif import_type == "Student Info":
                success = self.db_manager.import_student_info(file_path, file_type == "SQLite Database (.db)",
                                                              self.student_ids)
            else:  # Presence Info
                success = self.db_manager.import_presence_info(file_path, file_type == "SQLite Database (.db)")

            if success:
                self.lessons = self.db_manager.load_lessons()
                self.update_lesson_combo()
                QMessageBox.information(self, "Success", f"{import_type} imported successfully.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to import {import_type}. Check file format and columns.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")

    def update_lesson_data(self, old_name, new_data):
        try:
            self.db_manager.update_lesson(old_name, new_data)
            self.lessons[new_data["name"]] = new_data
            if old_name != new_data["name"] and old_name in self.lessons:
                del self.lessons[old_name]
            self.update_lesson_combo()
            self.lesson_combo.setCurrentText(new_data["name"])
            self.update_lesson_info_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update lesson data: {str(e)}")