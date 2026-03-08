from infrastructure.repositories.payment_repository import PaymentRepository
from infrastructure.repositories.student_repository import StudentRepository


class PaymentUseCases:
    def __init__(self):
        self.payment_repo = PaymentRepository()
        self.student_repo = StudentRepository()

    def get_students_by_class(self, class_code) -> list:
        return self.student_repo.get_students_by_class(class_code)

    def save_payment(self, class_code, data) -> None:
        self.payment_repo.save_payment(class_code, data)

    def get_payment(self, class_code) -> list:
        return self.payment_repo.get_payment_by_class(class_code)
