from dataclasses import dataclass


@dataclass
class PaymentDTO:
    class_code: str
    student_id: str
    payment_code: str
    amount: str
    payment_date: str
    status: str
    note: str
