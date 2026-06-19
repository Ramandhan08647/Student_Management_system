from database.database import Database

class TeacherManager:
    def __init__(self, db: Database):
        self.db = db

    def add_teacher(self, teacher_id: str, full_name: str, qualification: str, department: str, subject: str, phone: str, email: str) -> int:
        now = self.db.current_timestamp()
        return self.db.insert(
            "INSERT INTO teachers (teacher_id, full_name, qualification, department, subject, phone, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (teacher_id, full_name, qualification, department, subject, phone, email, now, now),
        )

    def update_teacher(self, teacher_id: str, **fields) -> None:
        assignments = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = tuple(fields.values()) + (self.db.current_timestamp(), teacher_id)
        self.db.execute(f"UPDATE teachers SET {assignments}, updated_at = ? WHERE teacher_id = ?", values)

    def delete_teacher(self, teacher_id: str) -> None:
        self.db.execute("DELETE FROM teachers WHERE teacher_id = ?", (teacher_id,))

    def get_teacher(self, teacher_id: str) -> dict:
        row = self.db.fetchone("SELECT * FROM teachers WHERE teacher_id = ?", (teacher_id,))
        return dict(row) if row else None

    def search_teachers(self, search_term: str) -> list[dict]:
        term = f"%{search_term}%"
        rows = self.db.fetchall(
            "SELECT * FROM teachers WHERE teacher_id LIKE ? OR full_name LIKE ? OR email LIKE ? OR phone LIKE ?",
            (term, term, term, term),
        )
        return [dict(row) for row in rows]
