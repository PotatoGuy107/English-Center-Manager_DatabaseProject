class DSHocVienBLL:

    @staticmethod
    def validate_student(name, phone, email):

        if not name.strip():
            return False, "Tên không được để trống"

        if not phone.strip():
            return False, "SĐT không được để trống"

        if not phone.isdigit():
            return False, "SĐT phải là số"

        if len(phone) < 9:
            return False, "SĐT không hợp lệ"

        if not email.strip():
            return False, "Email không được để trống"

        if "@" not in email:
            return False, "Email không hợp lệ"

        return True, ""
