from MODELS.payment_model import Payment

class PaymentDAL:
    _payments = []

    def save_payment(self, class_code, data):

        for row in data:

            student_id = row[1]
            payment_code = row[3]
            amount = row[4]
            payment_date = row[5]
            status = row[6]
            note = row[7]

            if student_id.strip() == "":
                continue

            # Kiểm tra đã tồn tại chưa
            for p in self._payments:
                if (p.class_code == class_code and
                    p.student_id == student_id):

                    # update
                    p.payment_code = payment_code
                    p.amount = amount
                    p.payment_date = payment_date
                    p.status = status
                    p.note = note
                    break
            else:
                # thêm mới
                new_payment = Payment(
                    class_code,
                    student_id,
                    payment_code,
                    amount,
                    payment_date,
                    status,
                    note
                )
                self._payments.append(new_payment)

    def get_payment_by_class(self, class_code):
        return [
            p for p in self._payments
            if p.class_code == class_code
        ]