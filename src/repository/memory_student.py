from src.domain.student import Student
from src.exceptions.exceptions import StudentNotFoundError, DuplicateStudentError, InvalidStudentUpdateError

class StudentRepository:
    def __init__(self):
        self._students = {}

    def add_student(self, student):
        try:
            if student.id in self._students:
                raise DuplicateStudentError(f"Student with ID {student.id} already exists.")
            self._students[student.id] = student
        except DuplicateStudentError as e:
            print(f"Warning: Skipping student with ID {student.id}: {e}")

    def remove_student(self, student_id, grade_repo):
        if student_id not in self._students:
            raise StudentNotFoundError(f"Student with ID {student_id} does not exist.")

        # Remove the student
        del self._students[student_id]

        # Remove all grades for the student
        grade_repo.remove_grades_for_student(student_id)

    def find_student(self, student_id):
        student = self._students.get(student_id)  # Fetch student by ID
        if not student:  # Check if student is None or falsy
            raise StudentNotFoundError(f"Student with ID {student_id} not found.")
        return student
    def search_students(self, search_term):
        search_term = search_term.lower()
        return [student for student in self._students.values() if search_term in student.name.lower()]

    def list_all(self):
        return list(self._students.values())

    def update_student(self, student_id_inf: int, new_name: str = None, new_group: int = None):
        if not new_name and not new_group:
            raise InvalidStudentUpdateError("At least one of 'new_name' or 'new_group' must be provided for update.")

        studentel = self._students.get(student_id_inf)
        if not studentel:
            raise StudentNotFoundError(f"Student with ID {student_id} does not exist.")

        if new_name:
            studentel.name = new_name  # Use the property setter
        if new_group is not None:
            studentel.group = new_group  # Use the property setter

    def get_all_ids(self):
        """
        Return a list of all student IDs in the repository.
        """
        return list(self._students.keys())
# Example usage with Faker
if __name__ == "__main__":
    from faker import Faker
    fake = Faker()

    student_repo = StudentRepository()

    # Generate students
    for _ in range(20):
        name = fake.name()
        student_id = fake.random_int(min=1000, max=9999)
        group = fake.random_int(min=900, max=999)
        try:
            student = Student(name, student_id, group)
            student_repo.add_student(student)
        except DuplicateStudentError as e:
            print(f"Warning: Could not add student {name} with ID {student_id}: {e}")

    # List all students
    print("All students:")
    for student in student_repo.list_all():
        print(student)
