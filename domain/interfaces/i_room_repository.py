from abc import ABC, abstractmethod


class IRoomRepository(ABC):
    @abstractmethod
    def get_all_rooms(self) -> list:
        pass

    @abstractmethod
    def insert_room(self, data) -> None:
        pass

    @abstractmethod
    def update_status(self, room_id, new_status) -> None:
        pass
