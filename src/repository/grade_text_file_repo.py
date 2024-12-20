from src.domain.grade import Grade
from src.repository.memory_grade import GradeRepository


class GradeTextFileRepository(GradeRepository):
    def __init__(self, filename):
        super().__init__()
        self.__filename = filename
        self.__load_file()

    def __load_file(self):
        """
        Load grades from a text file into the repository.
        """
        try:
            with open(self.__filename, "rt") as file:
                for line in file:
                    parts = line.strip().split(",")
                    assignment_id = int(parts[0])
                    student_id = int(parts[1])
                    grade_value = None if parts[2] == "None" else float(parts[2])
                    self.grades[(assignment_id, student_id)] = grade_value
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty repository
            self.grades = {}

    def __save_file(self):
        """
        Save all grades from the repository to a text file.
        """
        with open(self.__filename, "wt") as file:
            for (assignment_id, student_id), grade_value in self.grades.items():
                grade_value_str = "None" if grade_value is None else str(grade_value)
                file.write(f"{assignment_id},{student_id},{grade_value_str}\n")

    def add_grade(self, student_id, assignment_id, grade_value):
        """
        Add a grade and save changes to the file.
        """
        super().add_grade(student_id, assignment_id, grade_value)
        self.__save_file()

    def update_grade(self, student_id, assignment_id, grade_value):
        """
        Update a grade and save changes to the file.
        """
        super().update_grade(student_id, assignment_id, grade_value)
        self.__save_file()

    def remove_grades_for_assignment(self, assignment_id):
        """
        Remove all grades for a specific assignment and save changes to the file.
        """
        super().remove_grades_for_assignment(assignment_id)
        self.__save_file()

    def remove_grades_for_student(self, student_id):
        """
        Remove all grades for a specific student and save changes to the file.
        """
        super().remove_grades_for_student(student_id)
        self.__save_file()

    def get_grades_for_student(self, student_id):
        """
        Retrieve assignments and grades for a student.
        """
        return super().get_grades_for_student(student_id)

    def get_assignments_for_student(self, student_id):
        """
        Retrieve all assignments for a specific student.
        """
        return super().get_assignments_for_student(student_id)

    def get_grade_for_assig(self, student_id, assignment_id):
        """
        Retrieve a specific grade for a given student and assignment.
        """
        return super().get_grade_for_assig(student_id, assignment_id)

