from datetime import datetime
from typing import Optional

from database.database import Database

class StudentManager:
    def __init__(self, db: Database):
        self.db = db

    def generate_student_id(self) -> str:
        year = datetime.now().year
        count = self.db.fetchone("SELECT COUNT(*) as total FROM students", ())
        next_number = (count["total"] if count else 0) + 1
        return f"STD-{year}-{next_number:04d}"

    def add_student(self, first_name: str, last_name: str, gender: str, dob: str, address: str, nationality: str, class_name: str, department: str, email: str, phone: str, parent_name: str, parent_phone: str, photo_path: str = None) -> int:
        student_id = self.generate_student_id()
        now = self.db.current_timestamp()
        return self.db.insert(
            "INSERT INTO students (student_id, first_name, last_name, gender, dob, address, nationality, class, department, email, phone, parent_name, parent_phone, photo_path, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (student_id, first_name, last_name, gender, dob, address, nationality, class_name, department, email, phone, parent_name, parent_phone, photo_path, now, now),
        )

    def update_student(self, student_id: str, **fields) -> None:
        assignments = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = tuple(fields.values()) + (self.db.current_timestamp(), student_id)
        self.db.execute(f"UPDATE students SET {assignments}, updated_at = ? WHERE student_id = ?", values)

    def delete_student(self, student_id: str) -> None:
        self.db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))

    def get_student(self, student_id: str) -> Optional[dict]:
        row = self.db.fetchone("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return dict(row) if row else None

    def search_students(self, search_term: str) -> list[dict]:
        term = f"%{search_term}%"
        rows = self.db.fetchall(
            "SELECT * FROM students WHERE student_id LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ?",
            (term, term, term, term, term),
        )
        return [dict(row) for row in rows]
