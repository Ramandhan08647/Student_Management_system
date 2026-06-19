from datetime import datetime
from typing import Dict, Any, List

class FeeManager:
    def __init__(self, db=None):
        self.db = db

    def add_payment(self, student_id: str, amount_paid: float, payment_method: str, balance: float) -> Dict[str, Any]:
        payment = {
            "receipt_number": f"RCPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "student_id": student_id,
            "amount_paid": amount_paid,
            "balance": balance,
            "payment_method": payment_method,
            "payment_date": datetime.now().isoformat(),
        }
        return payment

    def get_payment_history(self, student_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "receipt_number": "RCPT-202606170001",
                "student_id": student_id,
                "amount_paid": 500.0,
                "balance": 1500.0,
                "payment_date": datetime.now().isoformat(),
            }
        ]
