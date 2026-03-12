from abc import ABC, abstractmethod


class IAuthRepository(ABC):
    @abstractmethod
    def check_login(self, username, password) -> dict | None:
        pass
