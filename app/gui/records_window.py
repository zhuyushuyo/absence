from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton

class RecordsWindow(QMainWindow):
    def __init__(self, summary_text, absence_details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Submission Records")
        self.setGeometry(150, 150, 600, 400)
        self.absence_details = absence_details

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(summary_text)
        layout.addWidget(self.text_edit)

        if any(details for details in absence_details.values()):
            self.show_absences_button = QPushButton("Show Absence Details")
            self.show_absences_button.clicked.connect(self.show_absence_details)
            layout.addWidget(self.show_absences_button)

    def show_absence_details(self):
        detail_text = []
        for key, details in self.absence_details.items():
            if details:
                date, lesson, day, period = key
                detail_text.append(f"Date: {date}, Lesson: {lesson}, Day: {day}, Period: {period}")
                detail_text.append("Absent Students:")
                for student_id in details:
                    detail_text.append(f"  - {student_id}")
                detail_text.append("")
        self.text_edit.setText("\n".join(detail_text))
        self.show_absences_button.hide()