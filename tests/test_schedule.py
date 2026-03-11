"""Test schedule functionality"""
import traceback

try:
    from infrastructure.repositories.schedule_repository import ScheduleRepository
    from application.use_cases.schedule_use_cases import ScheduleUseCases
    
    print("Testing ScheduleRepository.get_all()...")
    schedules = ScheduleRepository.get_all()
    print(f"Found {len(schedules)} schedules")
    for s in schedules[:3]:
        print(f"  {s}")
    
    print("\nTesting ScheduleUseCases.get_all_schedules()...")
    use_cases = ScheduleUseCases()
    schedules = use_cases.get_all_schedules()
    print(f"Found {len(schedules)} schedules")
    
    print("\nAll tests passed!")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
