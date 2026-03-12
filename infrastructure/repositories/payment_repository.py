from domain.entities.payment_entity import Payment
from domain.interfaces.i_payment_repository import IPaymentRepository
from infrastructure.config.database import get_connection


class PaymentRepository(IPaymentRepository):
    """Manages Payment records in SQL Server.
    Schema: payment_id VARCHAR(10), enrollment_id VARCHAR(10), payment_date DATE, 
            amount DECIMAL(12,2), payment_status VARCHAR(20), note NVARCHAR(255)
    """

    @staticmethod
    def get_next_payment_id() -> str:
        """Generate next payment_id like PM001, PM002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(payment_id, 3, LEN(payment_id)-2) AS INT)) FROM Payment WHERE payment_id LIKE 'PM%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"PM{max_num + 1:03d}"

    @staticmethod
    def get_all_payments() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.payment_id, p.enrollment_id, e.student_id, s.full_name, 
                   p.amount, p.payment_date, p.payment_status, p.note
            FROM Payment p
            LEFT JOIN Enrollment e ON p.enrollment_id = e.enrollment_id
            LEFT JOIN Student s ON e.student_id = s.student_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(payment_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT payment_id, enrollment_id, amount, payment_date, payment_status, note 
            FROM Payment WHERE payment_id=?
        """, (payment_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_by_enrollment(enrollment_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT payment_id, enrollment_id, amount, payment_date, payment_status, note
            FROM Payment WHERE enrollment_id=?
        """, (enrollment_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_payments_by_student(student_id) -> list:
        """Get all payments for a student through their enrollments"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.payment_id, e.student_id, c.course_name, p.amount, 
                   p.payment_date, p.payment_status, p.note
            FROM Payment p
            JOIN Enrollment e ON p.enrollment_id = e.enrollment_id
            JOIN Course c ON e.course_id = c.course_id
            WHERE e.student_id=?
        """, (student_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> str:
        """Insert payment. data = (payment_id, enrollment_id, amount, payment_date, payment_status, note). Returns payment_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Payment (payment_id, enrollment_id, amount, payment_date, payment_status, note) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

    @staticmethod
    def update(data) -> None:
        """Update payment. data = (payment_id, enrollment_id, amount, payment_date, payment_status, note)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Payment
            SET enrollment_id=?, amount=?, payment_date=?, payment_status=?, note=?
            WHERE payment_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(payment_id, status) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Payment SET payment_status=? WHERE payment_id=?", (status, payment_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(payment_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Payment WHERE payment_id=?", (payment_id,))
        conn.commit()
        conn.close()

    # Legacy methods for backward compatibility
    def save_payment(self, class_code, data) -> None:
        """Legacy method - save payments by class. Tries to find enrollment from class_enrollment."""
        conn = get_connection()
        cursor = conn.cursor()
        
        for row in data:
            student_id = row[1] if len(row) > 1 else None
            if not student_id:
                continue
            
            # Try to find enrollment for this student
            cursor.execute("""
                SELECT e.enrollment_id FROM Enrollment e
                JOIN Class_Enrollment ce ON e.student_id = ce.student_id 
                    AND e.course_id = (SELECT sk.course_id FROM Class c 
                                       JOIN Skill sk ON c.skill_id = sk.skill_id 
                                       WHERE c.class_id = ?)
                WHERE e.student_id = ?
            """, (class_code, student_id))
            enrollment_row = cursor.fetchone()
            enrollment_id = enrollment_row[0] if enrollment_row else None

            payment_id = row[3] if len(row) > 3 else self.get_next_payment_id()
            amount = row[4] if len(row) > 4 else 0
            payment_date = row[5] if len(row) > 5 else None
            status = row[6] if len(row) > 6 else 'Unpaid'
            note = row[7] if len(row) > 7 else None

            # Check if payment exists
            cursor.execute("SELECT payment_id FROM Payment WHERE payment_id=?", (payment_id,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("""
                    UPDATE Payment SET amount=?, payment_date=?, payment_status=?, note=?
                    WHERE payment_id=?
                """, (amount, payment_date, status, note, payment_id))
            else:
                new_payment_id = PaymentRepository.get_next_payment_id()
                cursor.execute("""
                    INSERT INTO Payment (payment_id, enrollment_id, amount, payment_date, payment_status, note)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (new_payment_id, enrollment_id, amount, payment_date, status, note))
        
        conn.commit()
        conn.close()

    def get_payment_by_class(self, class_code) -> list:
        """Legacy method - get payments for students in a class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ce.class_id, ce.student_id, s.full_name, p.payment_id, 
                   p.amount, p.payment_date, p.payment_status, p.note
            FROM Class_Enrollment ce
            JOIN Student s ON ce.student_id = s.student_id
            JOIN Enrollment e ON e.student_id = ce.student_id 
                AND e.course_id = (SELECT sk.course_id FROM Class c 
                                   JOIN Skill sk ON c.skill_id = sk.skill_id 
                                   WHERE c.class_id = ce.class_id)
            LEFT JOIN Payment p ON p.enrollment_id = e.enrollment_id
            WHERE ce.class_id = ?
        """, (class_code,))
        rows = cursor.fetchall()
        conn.close()
        
        payments = []
        for r in rows:
            payments.append(Payment(r[0], r[1], r[3], r[4], r[5], r[6], r[7] if len(r) > 7 else None))
        return payments
