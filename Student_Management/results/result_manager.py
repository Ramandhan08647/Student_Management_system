from datetime import datetime
from typing import Dict, Any

class ResultManager:
    def __init__(self, db=None):
        self.db = db

    def calculate_result(self, test_score: float, assignment_score: float, exam_score: float) -> Dict[str, Any]:
        total_score = test_score + assignment_score + exam_score
        percentage = total_score / 3
        grade = self._grade_from_percentage(percentage)
        gpa = self._gpa_from_grade(grade)
        return {
            "test_score": test_score,
            "assignment_score": assignment_score,
            "exam_score": exam_score,
            "total_score": total_score,
            "percentage": round(percentage, 2),
            "grade": grade,
            "gpa": gpa,
            "remarks": "Result computed successfully",
            "generated_at": datetime.now().isoformat(),
        }

    def _grade_from_percentage(self, percentage: float) -> str:
        if percentage >= 70:
            return "A"
        if percentage >= 60:
            return "B"
        if percentage >= 50:
            return "C"
        if percentage >= 45:
            return "D"
        if percentage >= 40:
            return "E"
        return "F"

    def _gpa_from_grade(self, grade: str) -> float:
        mapping = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.7, "F": 0.0}
        return mapping.get(grade, 0.0)
