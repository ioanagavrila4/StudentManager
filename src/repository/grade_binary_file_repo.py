import pickle
from src.domain.grade import Grade
from src.repository.memory_grade import GradeRepository

class GradeBinaryFileRepository(GradeRepository):
    def __init__(self, filename):
        super().__init__()
        self.__fileName = filename
        self.__load_file()

    def __load_file(self):
        """Load grades from a binary file."""
        try:
            with open(self.__fileName, "rb") as file:
                self.grades = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.grades = []

    def __save_file(self):
        """Save all grades to a binary file."""
        with open(self.__fileName, "wb") as file:
            pickle.dump(self.grades, file)

    def add_grade(self, student_id, assignment_id, grade_value):
        super().add_grade(student_id, assignment_id, grade_value)
        self.__save_file()

    def remove_grades_for_student(self, student_id):
        super().remove_grades_for_student(student_id)
        self.__save_file()

    def remove_grades_for_assignment(self, assignment_id):
        super().remove_grades_for_assignment(assignment_id)
        self.__save_file()
