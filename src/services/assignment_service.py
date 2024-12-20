from src.repository.memory_student import StudentRepository
from src.repository.memory_assignment import AssignmentRepository
from src.repository.memory_grade import GradeRepository
from src.services.student_service import StudentService
from src.services.grade_service import GradeService
from src.domain.student import Student
from src.domain.assigment import Assignment
from src.domain.grade import Grade
from datetime import datetime

from src.services.undo_service import UndoService, FunctionCall, Operation

class AssignmentService:
    def __init__(self, assignment_repo: AssignmentRepository, student_repo: StudentRepository, undo_service: UndoService):
        self._assignment_repo = assignment_repo
        self._student_repo = student_repo
        self._undo_service = undo_service
        self._student_assignments = {}  # Tracks assignments given to students {student_id: [assignment_id, ...]}

    def get_assignment(self, assignment_id: int):
        """
        Fetches an assignment by ID.
        :param assignment_id: The ID of the assignment.
        :return: The assignment object.
        """
        return self._assignment_repo.get(assignment_id)

    def add_assignment(self, assignment: Assignment):
        """
        Adds an assignment to the repository.
        :param assignment: The assignment object to add.
        """
        # Define undo and redo functions for adding an assignment
        def undo_add():
            self._assignment_repo.remove_assignment(assignment.id, grade_repo=None)

        def redo_add():
            self._assignment_repo.add_assignment(assignment)

        # Add the assignment
        self._assignment_repo.add_assignment(assignment)

        # Record the operation for undo/redo
        undo_function = FunctionCall(undo_add)
        redo_function = FunctionCall(redo_add)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)
    def remove_assignment(self, assignment_id: int, grade_repo: GradeRepository):
        """
        Removes an assignment from the repository and deletes all grades associated with it.
        :param assignment_id: The ID of the assignment to remove.
        :param grade_repo: The grade repository to remove associated grades.
        """
        # Fetch the assignment to remove
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} not found.")

        # Define undo and redo functions for removing an assignment
        def undo_remove():
            self._assignment_repo.add_assignment(assignment)

        def redo_remove():
            self._assignment_repo.remove_assignment(assignment_id, grade_repo)

        # Remove the assignment and associated grades
        grade_repo.remove_grades_for_assignment(assignment_id)
        self._assignment_repo.remove_assignment(assignment_id, grade_repo)

        # Record the operation for undo/redo
        undo_function = FunctionCall(undo_remove)
        redo_function = FunctionCall(redo_remove)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)
    def update_assignment(self, assignment_id: int, new_description: str = None, new_deadline: str = None):
        """
        Updates an assignment's description and/or deadline in the repository.
        :param assignment_id: The ID of the assignment to update.
        :param new_description: The new description for the assignment. If None, it won't be updated.
        :param new_deadline: The new deadline for the assignment. If None, it won't be updated.
        """
        # Fetch the assignment to update
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} not found.")

        # Save the current state for undo functionality
        old_description = assignment.description
        old_deadline = assignment.deadline

        # Define undo and redo functions for updating an assignment
        def undo_update():
            assignment.description = old_description
            assignment.deadline = old_deadline
            self._assignment_repo.update_assignment(assignment)

        def redo_update():
            if new_description:
                assignment.description = new_description
            if new_deadline:
                assignment.deadline = new_deadline
            self._assignment_repo.update_assignment(assignment)

        # Update the assignment
        if new_description:
            assignment.description = new_description
        if new_deadline:
            assignment.deadline = new_deadline

        # Save the updated assignment
        self._assignment_repo.update_assignment(assignment)

        # Record the operation for undo/redo
        undo_function = FunctionCall(undo_update)
        redo_function = FunctionCall(redo_update)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)


    def assign_to_students(self, assignment_id: int, student_ids: list[int]):
        """
        Assigns an assignment to a list of students. If a student already has the assignment, it will not be added again.
        :param assignment_id: The ID of the assignment to assign.
        :param student_ids: A list of student IDs to assign the assignment to.
        """
        # Validate assignment existence
        assignment = self._assignment_repo.get(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} does not exist.")

        students_before = {student_id: self._student_assignments.get(student_id, []) for student_id in student_ids}

        def undo_assign():
            for student_id in student_ids:
                if student_id in self._student_assignments:
                    self._student_assignments[student_id] = students_before.get(student_id, [])

        def redo_assign():
            for student_id in student_ids:
                if student_id not in self._student_assignments:
                    self._student_assignments[student_id] = []
                if assignment_id not in self._student_assignments[student_id]:
                    self._student_assignments[student_id].append(assignment_id)

        # Perform the actual assignment
        for student_id in student_ids:
            if student_id not in self._student_assignments:
                self._student_assignments[student_id] = []
            if assignment_id not in self._student_assignments[student_id]:
                self._student_assignments[student_id].append(assignment_id)

        # Record the operation for undo/redo
        undo_function = FunctionCall(undo_assign)
        redo_function = FunctionCall(redo_assign)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)

    def assign_to_group(self, assignment_id: int, group: int):
        """
        Assigns an assignment to all students in a specific group.
        :param assignment_id: The ID of the assignment to assign.
        :param group: The group number to assign the assignment to.
        """
        # Get all students in the group
        students_in_group = [
            student.id for student in self._student_repo.list_all() if student.group == group
        ]
        if not students_in_group:
            raise ValueError(f"No students found in group {group}.")
        # Assign to all students in the group
        self.assign_to_students(assignment_id, students_in_group)

    def list_student_assignments(self, student_id: int):
        """
        Returns the list of assignments for a specific student.
        :param student_id: The ID of the student.
        :return: List of assignment IDs.
        """
        if student_id not in self._student_assignments:
            return []
        return self._student_assignments[student_id]

    def list_all_assignments(self):
        """
        Fetches and returns all assignments from the repository.
        :return: A list of all assignment objects.
        """
        return self._assignment_repo.list_assignments()

    def get_students_late_with_assignments(self, grade_repo: GradeRepository):
        """
        Get all students who are late in handing in at least one assignment.
        Late means an ungraded assignment for which the deadline has passed.
        :param grade_repo: The grade repository to check for grades.
        :return: List of students who are late.
        """
        from datetime import datetime

        late_students = set()

        for student_id, assignment_ids in self._student_assignments.items():
            for assignment_id in assignment_ids:
                assignment = self._assignment_repo.get(assignment_id)

                # Check if the assignment exists and has a valid deadline
                if not assignment:
                    continue

                # Check if the grade is None (ungraded) and the deadline has passed
                grade = grade_repo.get_grade_for_assig(student_id, assignment_id)
                if grade is None and datetime.strptime(assignment.deadline, "%Y-%m-%d") < datetime.now():
                    student = self._student_repo.find_student(student_id)
                    if student:
                        late_students.add(student)

        return list(late_students)

    def get_assignments_for_student(self, student_id: int):
        return [
            assignment_id for assignment_id, students in self._student_assignments.items()
            if student_id in students
        ]
