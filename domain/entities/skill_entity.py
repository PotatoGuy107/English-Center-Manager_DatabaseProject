class Skill:
    """Skill entity matching SQL Server Skill table"""
    def __init__(
        self,
        skill_id: int = None,
        course_id: int = None,
        skill_name: str = "",
        description: str = None,
    ):
        self.skill_id = skill_id
        self.course_id = course_id
        self.skill_name = skill_name
        self.description = description
