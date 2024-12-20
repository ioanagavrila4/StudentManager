from src.repository.memory_assignment import AssignmentRepository
from src.domain.assigment import Assignment


class AssignmentTextFileRepository(AssignmentRepository):
    def __init__(self, filename):
        super().__init__()
        self.__fileName = filename
        self.__loadFile()

    def __loadFile(self):
        """
        Load assignments from a text file.
        """
        lines = []
        try:
            with open(self.__fileName, "rt") as fin:
                lines = fin.readlines()
        except IOError:
            # It's okay if the file doesn't exist yet
            pass

        for line in lines:
            current_line = line.strip().split(",")
            new_assignment = Assignment(
                int(current_line[0]),  # ID
                current_line[1],       # Description
                current_line[2]        # Deadline
            )
            self.assignments[new_assignment.id] = new_assignment

    def __saveFile(self):
        """
        Save all assignments to a text file.
        """
        with open(self.__fileName, "wt") as fout:
            for assignment in self.list_assignments():
                assignment_string = f"{assignment.id},{assignment.description},{assignment.deadline}\n"
                fout.write(assignment_string)

    def add_assignment(self, assignment):
        """
        Add a new assignment to the repository and save to file.
        """
        super().add_assignment(assignment)
        self.__saveFile()

    def remove_assignment(self, assignment_id, grade_repo):
        """
        Remove an assignment by ID and save changes to file.
        """
        super().remove_assignment(assignment_id, grade_repo)
        self.__saveFile()

    def update_assignment(self, assignment):
        """
        Update an existing assignment and save changes to file.
        """
        super().update_assignment(assignment)
        self.__saveFile()

    def give_assignment_to_student(self, assignment_id, student_id, grade_repo):
        """
        Assign an assignment to a specific student and save to file.
        """
        super().give_assignment_to_student(assignment_id, student_id, grade_repo)
        self.__saveFile()

    def give_assignment_to_group(self, assignment_id, group_id, student_repo, grade_repo):
        """
        Assign an assignment to a group of students and save to file.
        """
        super().give_assignment_to_group(assignment_id, group_id, student_repo, grade_repo)
        self.__saveFile()
