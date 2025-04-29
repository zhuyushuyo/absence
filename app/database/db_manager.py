import sqlite3
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS submissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        lesson TEXT,
                        day TEXT,
                        period TEXT,
                        student_id TEXT,
                        status TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS lessons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        day TEXT,
                        period TEXT,
                        begin_date TEXT,
                        end_date TEXT
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to initialize database: {str(e)}")

    def load_lessons(self):
        lessons = {}
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT name, day, period, begin_date, end_date FROM lessons')
                for name, day, period, begin_date, end_date in cursor.fetchall():
                    begin_date_obj = QDate.fromString(begin_date, "yyyy-MM-dd")
                    end_date_obj = QDate.fromString(end_date, "yyyy-MM-dd")
                    lessons[name] = {
                        "name": name,
                        "day": day,
                        "period": period,
                        "begin_date": begin_date_obj,
                        "end_date": end_date_obj
                    }
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to load lessons: {str(e)}")
        return lessons

    def update_lesson(self, old_name, new_data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if old_name:
                    cursor.execute('''
                        UPDATE lessons SET name = ?, day = ?, period = ?, begin_date = ?, end_date = ?
                        WHERE name = ?
                    ''', (new_data["name"], new_data["day"], new_data["period"],
                          new_data["begin_date"].toString("yyyy-MM-dd"),
                          new_data["end_date"].toString("yyyy-MM-dd"), old_name))
                else:
                    cursor.execute('''
                        INSERT INTO lessons (name, day, period, begin_date, end_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (new_data["name"], new_data["day"], new_data["period"],
                          new_data["begin_date"].toString("yyyy-MM-dd"),
                          new_data["end_date"].toString("yyyy-MM-dd")))
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to update lesson: {str(e)}")

    def save_submissions(self, submissions):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany('''
                    INSERT INTO submissions (date, lesson, day, period, student_id, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', submissions)
                conn.commit()
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to save submissions: {str(e)}")
            return False

    def fetch_records(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT date, lesson, day, period, student_id, status FROM submissions')
                return cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to read records: {str(e)}")
            return []

    def fetch_submissions_for_export(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT date, lesson, day, period, student_id, status FROM submissions')
                return cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error", f"Failed to fetch submissions: {str(e)}")
            return []

    def import_lesson_info(self, file_path, is_db):
        try:
            if is_db:
                with sqlite3.connect(file_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT name, day, period, begin_date, end_date FROM lessons')
                    rows = cursor.fetchall()
                for row in rows:
                    name, day, period, begin_date, end_date = row
                    begin_date_obj = QDate.fromString(begin_date, "yyyy-MM-dd")
                    end_date_obj = QDate.fromString(end_date, "yyyy-MM-dd")
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT OR REPLACE INTO lessons (name, day, period, begin_date, end_date)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (name, day, period, begin_date, end_date))
                        conn.commit()
            else:  # Excel
                df = pd.read_excel(file_path)
                required_columns = ["name", "day", "period", "begin_date", "end_date"]
                if not all(col in df.columns for col in required_columns):
                    return False
                for _, row in df.iterrows():
                    name = str(row["name"])
                    day = str(row["day"])
                    period = str(row["period"])
                    begin_date = str(row["begin_date"])
                    end_date = str(row["end_date"])
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT OR REPLACE INTO lessons (name, day, period, begin_date, end_date)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (name, day, period, begin_date, end_date))
                        conn.commit()
            return True
        except Exception as e:
            return False

    def import_student_info(self, file_path, is_db, student_ids):
        try:
            if is_db:
                with sqlite3.connect(file_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT student_id FROM students')
                    rows = cursor.fetchall()
                for row in rows:
                    student_id = row[0]
                    if student_id not in student_ids:
                        student_ids.append(student_id)
            else:  # Excel
                df = pd.read_excel(file_path)
                if "student_id" not in df.columns:
                    return False
                for _, row in df.iterrows():
                    student_id = str(row["student_id"])
                    if student_id not in student_ids:
                        student_ids.append(student_id)
            return True
        except Exception as e:
            return False

    def import_presence_info(self, file_path, is_db):
        try:
            if is_db:
                with sqlite3.connect(file_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT date, lesson, day, period, student_id, status FROM submissions')
                    rows = cursor.fetchall()
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.executemany('''
                        INSERT INTO submissions (date, lesson, day, period, student_id, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', rows)
                    conn.commit()
            else:  # Excel
                df = pd.read_excel(file_path)
                required_columns = ["date", "lesson", "day", "period", "student_id", "status"]
                if not all(col in df.columns for col in required_columns):
                    return False
                rows = [(str(row["date"]), str(row["lesson"]), str(row["day"]), str(row["period"]),
                         str(row["student_id"]), str(row["status"])) for _, row in df.iterrows()]
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.executemany('''
                        INSERT INTO submissions (date, lesson, day, period, student_id, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', rows)
                    conn.commit()
            return True
        except Exception as e:
            return False