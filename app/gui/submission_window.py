from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, \
    QMessageBox, QDateEdit
from PyQt6.QtCore import QDate
from ..database.db_manager import DatabaseManager


class SubmissionWindow(QMainWindow):
    def __init__(self, student_ids, lesson_data, present_students, db_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Submission")
        self.setGeometry(200, 200, 400, 400)
        self.student_ids = student_ids
        self.lesson_data = lesson_data
        self.present_students = present_students
        self.db_manager = db_manager
        self.parent = parent

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Date selector for submission
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addWidget(self.date_edit)

        self.student_list = QListWidget()
        self.student_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for student_id in self.student_ids:
            item = QListWidgetItem(student_id)
            item.setData(1, student_id)
            self.student_list.addItem(item)
        layout.addWidget(self.student_list)

        button_layout = QHBoxLayout()
        self.submit_presence_button = QPushButton("Submit Presence")
        self.submit_presence_button.clicked.connect(self.submit_presence)
        self.final_submit_button = QPushButton("Final Submission")
        self.final_submit_button.clicked.connect(self.final_submission)
        button_layout.addWidget(self.submit_presence_button)
        button_layout.addWidget(self.final_submit_button)
        layout.addLayout(button_layout)

    def submit_presence(self):
        try:
            selected_items = self.student_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "No Selection", "Please select at least one student.")
                return

            for item in selected_items:
                student_id = item.data(1)
                self.present_students.add(student_id)

            QMessageBox.information(self, "Success", f"Presence recorded for {len(selected_items)} student(s).")
            self.student_list.clearSelection()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit presence: {str(e)}")

    def final_submission(self):
        try:
            if not self.lesson_data.get("name"):
                QMessageBox.warning(self, "Missing Input", "Please set a lesson name in Edit Lesson Info.")
                return

            reply = QMessageBox.question(self, "Confirm Final Submission",
                                         "This is the final submission. Students not marked present will be recorded as absent. Proceed?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                date = self.date_edit.date().toString("yyyy-MM-dd")
                lesson = self.lesson_data["name"]
                day = self.lesson_data["day"]
                period = self.lesson_data["period"]

                submissions = []
                for student_id in self.student_ids:
                    status = "Present" if student_id in self.present_students else "Absent"
                    submissions.append((date, lesson, day, period, student_id, status))

                if self.db_manager.save_submissions(submissions):
                    self.present_students.clear()
                    QMessageBox.information(self, "Success", "Final submission completed. Records saved.")
                    self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to complete final submission: {str(e)}")