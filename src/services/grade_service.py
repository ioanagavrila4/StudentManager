from src.repository.memory_student import StudentRepository
from src.repository.memory_assignment import AssignmentRepository
from src.repository.memory_grade import GradeRepository
from src.services.student_service import StudentService
from src.domain.student import Student
from src.domain.assigment import Assignment
from datetime import datetime, date

from src.services.undo_service import FunctionCall, Operation, UndoService


class GradeService:
    def __init__(self, grade_repo: GradeRepository, student_repo: StudentRepository, assignment_repo: AssignmentRepository, undo_service: UndoService ):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._assignment_repo = assignment_repo
        self._undo_service = undo_service

    def grade_student(self, student_id: int, assignment_id: int, grade_value: int):
        """
        Grades a student for a given assignment.
        """
        # Validate the student exists
        student = self._student_repo.find_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        # Validate the assignment exists
        assignment = self._assignment_repo.get(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} does not exist.")

        # Add a default grade of None if not already present
        if assignment_id not in self._grade_repo.get_assignments_for_student(student_id):
            self._grade_repo.add_grade(student_id, assignment_id, None)

        # Ensure the grade is not already set
        current_grade = self._grade_repo.get_grade_for_assig(student_id, assignment_id)
        if current_grade is not None:
            raise ValueError(f"Student {student_id} has already been graded for assignment {assignment_id}.")

        # Define undo and redo functions
        def undo_grade():
            self._grade_repo.update_grade(student_id, assignment_id, None)  # Undo grading by setting to None

        def redo_grade():
            self._grade_repo.update_grade(student_id, assignment_id, grade_value)  # Redo grading with the original grade

        # Perform the actual grading operation
        self._grade_repo.update_grade(student_id, assignment_id, grade_value)

        # Record the undo/redo operation
        undo_function = FunctionCall(undo_grade)
        redo_function = FunctionCall(redo_grade)
        operation = Operation(undo_function, redo_function)
        self._undo_service.record(operation)

    def get_ungraded_assignments_for_student(self, student_id: int):
        """
        Returns a list of ungraded assignments for a student.
        """
        # Validate the student exists
        student = self._student_repo.find_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")

        # Get all assignments assigned to the student
        all_assignments = self._grade_repo.get_assignments_for_student(student_id)

        # Check the grade values for each assignment
        ungraded_assignments = []
        for assignment_id in all_assignments:
            grade_value = self._grade_repo.get_grade_for_assig(student_id, assignment_id)
            if grade_value is None:  # Only include ungraded assignments
                ungraded_assignments.append(assignment_id)

        return ungraded_assignments

    def get_students_with_assignment_ordered_by_grade(self, assignment_id: int):
        """
        Get all students who received a given assignment, ordered descending by grade.
        """

        assignment = self._assignment_repo.get(assignment_id)
        if not assignment:
            raise ValueError(f"Assignment with ID {assignment_id} does not exist.")

        students_with_grades = []
        for (assign_id, student_id), grade_value in self._grade_repo.grades.items():
            if assign_id == assignment_id:
                student = self._student_repo.find_student(student_id)
                if student:
                    grade = grade_value if grade_value is not None else 0  # Treat None grades as 0
                    students_with_grades.append((student, grade))

        # Sort students by grade descending
        return sorted(students_with_grades, key=lambda x: x[1], reverse=True)

    def remove_grade(self, student_id, assignment_id):
        # Validate that the grade exists
        grade = self._grade_repo.find_by_student_and_assignment(student_id, assignment_id)
        if not grade:
            raise ValueError(f"No grade found for student {student_id} and assignment {assignment_id}.")

        # Remove the grade
        self._grade_repo.delete(student_id, assignment_id)
    def get_students_sorted_by_average_grade(self):
        """
        Get students sorted in descending order of the average grade received for all graded assignments.
        """
        student_grades = {}

        # Collect grades for each student
        for (assignment_id, student_id), grade_value in self._grade_repo.grades.items():
            # Treat None grades as 0 for average calculation
            if student_id not in student_grades:
                student_grades[student_id] = []
            student_grades[student_id].append(grade_value if grade_value is not None else 0)

        # Include students with no grades
        for student_id in self._student_repo.get_all_ids():
            if student_id not in student_grades:
                student_grades[student_id] = []

        # Calculate averages
        student_averages = []
        for student_id, grades in student_grades.items():
            avg_grade = sum(grades) / len(grades) if grades else 0.0
            student = self._student_repo.find_student(student_id)
            if student:
                student_averages.append((student, avg_grade))

        # Sort by average grade descending
        return sorted(student_averages, key=lambda x: x[1], reverse=True)

    def get_late_students_with_ungraded_assignments(self):
        late_students = []

        # Get all students
        students = self._student_repo.list_all()

        for student in students:
            student_id = student.id

            # Get ungraded assignments for the student
            ungraded_assignments = self._assignment_repo.get_ungraded_assignments_for_student(student_id,
                                                                                              self._grade_repo)

            for assignment_id in ungraded_assignments:
                # Get the deadline for each assignment
                deadline = self._assignment_repo.get_deadline_for_assignment(assignment_id)

                # Check if the assignment's deadline has passed
                if isinstance(deadline, datetime):
                    assignment_deadline = deadline.date()
                elif isinstance(deadline, date):
                    assignment_deadline = deadline

                # Compare only dates (without time)
                if assignment_deadline < datetime.now().date():
                    late_students.append(student)
                    break  # No need to check further assignments for this student

        return late_students

    def get_students_with_best_grades(self):
        students_with_grades = []

        # Step 1: Get all students
        students = self._student_repo.list_all()

        # Step 2: Calculate the average grade for each student
        for student in students:
            student_id = student.id

            # Get all grades for this student
            grades = self._grade_repo.get_grades_for_student(student_id)

            # Calculate the average grade (exclude None grades)
            graded_assignments = [grade for grade in grades if grade[1] is not None]
            if graded_assignments:
                avg_grade = sum(grade[1] for grade in graded_assignments) / len(graded_assignments)
            else:
                avg_grade = 0  # No grades assigned

            students_with_grades.append((student, avg_grade))

        # Step 3: Sort students by average grade in descending order
        students_with_grades.sort(key=lambda x: x[1], reverse=True)

        return students_with_grades