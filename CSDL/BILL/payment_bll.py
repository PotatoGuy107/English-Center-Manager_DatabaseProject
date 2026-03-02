from DAL.payment_dal import PaymentDAL
from DAL.dshv_dal import FakeStudentRepository

class PaymentBLL:

    def __init__(self):
        self.payment_dal = PaymentDAL()
        self.student_repo = FakeStudentRepository()

    def get_students_by_class(self, class_code):
        return self.student_repo.get_students_by_class(class_code)

    def save_payment(self, class_code, data):
        self.payment_dal.save_payment(class_code, data)

    def get_payment(self, class_code):
        return self.payment_dal.get_payment_by_class(class_code)