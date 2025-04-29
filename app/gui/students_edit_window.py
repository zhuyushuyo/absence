from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QInputDialog, QMessageBox

class StudentsEditWindow(QMainWindow):
    def __init__(self, student_ids, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Students Info")
        self.setGeometry(200, 200, 400, 400)
        self.student_ids = student_ids
        self.parent = parent

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        self.student_list = QListWidget()
        self.update_student_list()
        layout.addWidget(self.student_list)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Student ID")
        self.add_button.clicked.connect(self.add_student)
        self.edit_button = QPushButton("Edit Selected ID")
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button = QPushButton("Delete Selected ID")
        self.delete_button.clicked.connect(self.delete_student)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

    def update_student_list(self):
        try:
            self.student_list.clear()
            for i, student_id in enumerate(self.student_ids, 1):
                item = QListWidgetItem(f"Student {i} (ID: {student_id})")
                self.student_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update student list: {str(e)}")

    def add_student(self):
        try:
            student_id, ok = QInputDialog.getText(self, "Add Student ID", "Enter new student ID:")
            if ok and student_id and student_id not in self.student_ids:
                self.student_ids.append(student_id)
                self.update_student_list()
                QMessageBox.information(self, "Success", f"Added student ID: {student_id}")
            elif ok and student_id in self.student_ids:
                QMessageBox.warning(self, "Duplicate ID", "This student ID already exists.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add student: {str(e)}")

    def edit_student(self):
        try:
            selected_items = self.student_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "No Selection", "Please select a student to edit.")
                return

            old_id = self.student_ids[self.student_list.row(selected_items[0])]
            new_id, ok = QInputDialog.getText(self, "Edit Student ID", "Enter new student ID:", text=old_id)
            if ok and new_id and new_id not in self.student_ids:
                index = self.student_ids.index(old_id)
                self.student_ids[index] = new_id
                self.update_student_list()
                QMessageBox.information(self, "Success", f"Changed student ID to: {new_id}")
            elif ok and new_id in self.student_ids:
                QMessageBox.warning(self, "Duplicate ID", "This student ID already exists.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit student: {str(e)}")

    def delete_student(self):
        try:
            selected_items = self.student_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "No Selection", "Please select a student to delete.")
                return

            student_id = self.student_ids[self.student_list.row(selected_items[0])]
            reply = QMessageBox.question(self, "Confirm Deletion",
                                        f"Delete student ID {student_id}?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.student_ids.remove(student_id)
                self.update_student_list()
                QMessageBox.information(self, "Success", f"Deleted student ID: {student_id}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete student: {str(e)}")

    def save_changes(self):
        try:
            if self.parent and hasattr(self.parent, 'update_lesson_info_display'):
                self.parent.update_lesson_info_display()
            QMessageBox.information(self, "Success", "Student IDs saved.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {str(e)}")