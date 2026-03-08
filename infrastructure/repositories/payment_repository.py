from domain.entities.payment_entity import Payment
from domain.interfaces.i_payment_repository import IPaymentRepository


class PaymentRepository(IPaymentRepository):
    _payments = []

    def save_payment(self, class_code, data) -> None:
        for row in data:
            student_id = row[1]
            if not student_id:
                continue
            payment_code = row[3]
            amount = row[4]
            payment_date = row[5]
            status = row[6]
            note = row[7]

            for p in self._payments:
                if p.class_code == class_code and p.student_id == student_id:
                    p.payment_code = payment_code
                    p.amount = amount
                    p.payment_date = payment_date
                    p.status = status
                    p.note = note
                    break
            else:
                self._payments.append(
                    Payment(class_code, student_id, payment_code, amount, payment_date, status, note)
                )

    def get_payment_by_class(self, class_code) -> list:
        return [p for p in self._payments if p.class_code == class_code]
