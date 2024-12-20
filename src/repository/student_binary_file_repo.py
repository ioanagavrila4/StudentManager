import pickle
from src.domain.student import Student
from src.repository.memory_student import StudentRepository

class StudentBinaryFileRepository(StudentRepository):
    def __init__(self, filename):
        super().__init__()
        self.__fileName = filename
        self.__load_file()

    def __load_file(self):
        """Load students from a binary file."""
        try:
            with open(self.__fileName, "rb") as file:
                self._students = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self._students = {}

    def __save_file(self):
        """Save all students to a binary file."""
        with open(self.__fileName, "wb") as file:
            pickle.dump(self._students, file)

    def add_student(self, student):
        super().add_student(student)
        self.__save_file()

    def remove_student(self, student_id, grade_repo):
        super().remove_student(student_id, grade_repo)
        self.__save_file()

    def update_student(self, student_id, new_name=None, new_group=None):
        updated_student = super().update_student(student_id, new_name, new_group)
        self.__save_file()
        return updated_student
