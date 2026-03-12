from abc import ABC, abstractmethod


class IPaymentRepository(ABC):
    @abstractmethod
    def save_payment(self, class_code, data) -> None:
        pass

    @abstractmethod
    def get_payment_by_class(self, class_code) -> list:
        pass
