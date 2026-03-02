class Payment:
    def __init__(self, class_code, student_id,
                 payment_code, amount,
                 payment_date, status, note):

        self.class_code = class_code
        self.student_id = student_id
        self.payment_code = payment_code
        self.amount = amount
        self.payment_date = payment_date
        self.status = status
        self.note = note