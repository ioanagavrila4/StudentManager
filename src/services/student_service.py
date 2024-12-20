from src.repository.memory_student import StudentRepository
from src.repository.memory_assignment import AssignmentRepository
from src.repository.memory_grade import GradeRepository
from src.domain.student import Student
from src.domain.assigment import Assignment
from src.services.undo_service import UndoService, FunctionCall, Operation

class StudentService:
    def __init__(self, repo: StudentRepository, grade_repo: GradeRepository,  undo_service: UndoService):
        self._repo = repo
        self._grade_repo = grade_repo
        self._undo_service = undo_service

    def get(self, student_id: int):
        return self._repo.find_student(student_id)

    def add(self, student: Student):
        def undo_add():
            self._repo.remove_student(student.id, self._grade_repo)

        def redo_add():
            self._repo.add_student(student)

        self._repo.add_student(student)

        undo_function = FunctionCall(undo_add)
        redo_function = FunctionCall(redo_add)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)

    def get_assignments_and_grades_for_student(self, student_id: int):
        student = self._repo.find_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")
        return self._grade_repo.get_grades_for_student(student_id)
    def get_student_by_id(self, student_id):
        return self._repo.find_student(student_id)
    def remove(self, student_id: int):
        student = self._repo.find_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        # Record the removal of a student
        def undo_remove():
            self._repo.add_student(student)  # Add student back
            # Restore the student's grades
            for assignment_id, grade in self._grade_repo.get_grades_for_student(student_id):
                self._grade_repo.add_grade(student.id, assignment_id, grade)

        def redo_remove():
            self._repo.remove_student(student.id, self._grade_repo)  # Remove student and grades
            self._grade_repo.remove_grades_for_student(student.id)

        # Perform the actual operation
        self._repo.remove_student(student.id, self._grade_repo)
        self._grade_repo.remove_grades_for_student(student.id)

        # Record the undo/redo operation
        undo_function = FunctionCall(undo_remove)
        redo_function = FunctionCall(redo_remove)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)

    def update(self, student_id: int, new_name: str = None, new_group: int = None):
        student = self.get(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found.")

        old_name = student.name
        old_group = student.group

        # Record the update operation
        def undo_update():
            self._repo.update_student(student_id, old_name, old_group)

        def redo_update():
            self._repo.update_student(student_id, new_name or student.name, new_group or student.group)

        # Perform the actual update operation
        self._repo.update_student(student_id, new_name or student.name, new_group or student.group)

        # Record the undo/redo operation
        undo_function = FunctionCall(undo_update)
        redo_function = FunctionCall(redo_update)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)


    def list_all(self):
        return self._repo.list_all()

    def get_all_student_ids(self):
        """
        Get a list of all student IDs.
        """
        return self._repo.get_all_ids()
