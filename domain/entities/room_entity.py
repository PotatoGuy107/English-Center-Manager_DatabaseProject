class Room:
    """Room entity matching SQL Server Room table"""
    def __init__(
        self,
        room_id: int = None,
        room_name: str = "",
        capacity: int = None,
        location: str = None,
        status: str = "Active",
    ):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self.location = location
        self.status = status
