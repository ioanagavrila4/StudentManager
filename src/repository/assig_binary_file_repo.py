import pickle
from src.domain.assigment import Assignment
from src.repository.memory_assignment import AssignmentRepository

class AssignmentBinaryFileRepository(AssignmentRepository):
    def __init__(self, filename):
        super().__init__()
        self.__fileName = filename
        self.__load_file()

    def __load_file(self):
        """Load assignments from a binary file."""
        try:
            with open(self.__fileName, "rb") as file:
                self.assignments = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.assignments = {}

    def __save_file(self):
        """Save all assignments to a binary file."""
        with open(self.__fileName, "wb") as file:
            pickle.dump(self.assignments, file)

    def add_assignment(self, assignment):
        super().add_assignment(assignment)
        self.__save_file()

    def remove_assignment(self, assignment_id, grade_repo):
        super().remove_assignment(assignment_id, grade_repo)
        self.__save_file()

    def update_assignment(self, assignment):
        super().update_assignment(assignment)
        self.__save_file()
