from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton

class ImportDetailsWindow(QMainWindow):
    def __init__(self, details_key, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import File Details")
        self.setGeometry(200, 200, 600, 400)
        self.details_key = details_key

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(self.get_details_text())
        layout.addWidget(self.text_edit)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

    def get_details_text(self):
        details = {
            "lesson_info": """
Lesson Info Import Details:
- File Format: SQLite Database (.db) or Excel (.xlsx)
- Required Columns:
  - name: Unique lesson name (text, e.g., "基礎セミナー")
  - day: Day of the week (text, e.g., "月曜日")
  - period: Class period (text, e.g., "1-2")
  - begin_date: Lesson start date (yyyy-MM-dd, e.g., "2025-04-01")
  - end_date: Lesson end date (yyyy-MM-dd, e.g., "2025-07-31")
- Notes:
  - For Excel, columns must match exactly (case-sensitive).
  - For DB, the lessons table must have the same schema as the app's database.
  - Duplicate lesson names will be skipped or updated if they match an existing entry.
""",
            "student_info": """
Student Info Import Details:
- File Format: SQLite Database (.db) or Excel (.xlsx)
- Required Column:
  - student_id: Unique student identifier (text, e.g., "NUS:022500203")
- Notes:
  - For Excel, ensure a single column named "student_id".
  - For DB, provide a table named "students" with a "student_id" column.
  - Duplicate IDs will be skipped to avoid conflicts.
""",
            "presence_info": """
Presence Info Import Details:
- File Format: SQLite Database (.db) or Excel (.xlsx)
- Required Columns:
  - date: Submission date (yyyy-MM-dd, e.g., "2025-04-29")
  - lesson: Lesson name (text, e.g., "基礎セミナー")
  - day: Day of the week (text, e.g., "月曜日")
  - period: Class period (text, e.g., "1-2")
  - student_id: Student identifier (text, e.g., "NUS:022500203")
  - status: Presence status (text, "Present" or "Absent")
- Notes:
  - For Excel, columns must match exactly (case-sensitive).
  - For DB, the submissions table must have the same schema as the app's database.
  - Ensure lesson and student IDs exist in the app before importing.
"""
        }
        return details.get(self.details_key, "No details available.")