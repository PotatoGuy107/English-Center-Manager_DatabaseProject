class Course:
    def __init__(self, course_id, name, description, credits):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.credits = credits

    def __repr__(self):
        return f"Course(course_id={self.course_id}, name='{self.name}', description='{self.description}', credits={self.credits})"