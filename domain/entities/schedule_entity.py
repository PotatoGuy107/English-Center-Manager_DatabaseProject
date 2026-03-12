from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Schedule:
    """Schedule entity matching database schema"""
    schedule_id: Optional[int] = None  # INT IDENTITY
    class_id: int = 0
    room_id: int = 0
    study_date: Optional[date] = None
    time_slot: Optional[str] = None  # e.g., "Ca 1", "Ca 2"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    # Optional joined data
    class_name: Optional[str] = None
    room_name: Optional[str] = None
    teacher_name: Optional[str] = None
    max_student: Optional[int] = None
    status: Optional[str] = None
