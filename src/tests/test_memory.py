import unittest
from src.domain.student import Student
from src.domain.assigment import Assignment
from src.domain.grade import Grade
from src.repository.memory_student import StudentRepository
from src.repository.memory_assignment import AssignmentRepository
from src.repository.memory_grade import GradeRepository

class TestMemoryStudentRepository(unittest.TestCase):
    def setUp(self):
        """Set up a fresh StudentRepository for each test."""
        self.repo = StudentRepository()

    def test_add_student(self):
        """Test adding a new student to the repository."""
        student = Student("Alice", 1234, 101)
        self.repo.add_student(student)
        self.assertEqual(len(self.repo.list_all()), 1, "Student was not added.")
        self.assertIn(student, self.repo.list_all(), "Added student is not in the repository.")

    # def test_add_duplicate_student(self):
    #     """Test that adding a student with a duplicate ID raises an error."""
    #     student1 = Student("Alice", 1234, 101)
    #     self.repo.add_student(student1)
    #     with self.assertRaises(ValueError):
    #         self.repo.add_student(student1)


class TestMemoryAssignmentRepository(unittest.TestCase):
    def setUp(self):
        """Set up a fresh AssignmentRepository for each test."""
        self.repo = AssignmentRepository()

    def test_add_assignment(self):
        """Test adding a new assignment to the repository."""
        assignment = Assignment(1, "Math Homework", "2023-12-15")
        self.repo.add_assignment(assignment)
        self.assertEqual(len(self.repo.list_assignments()), 1, "Assignment was not added.")
        self.assertIn(assignment, self.repo.list_assignments(), "Added assignment is not in the repository.")



class TestMemoryGradeRepository(unittest.TestCase):
    def setUp(self):
        """Set up a fresh GradeRepository for each test."""
        self.repo = GradeRepository()

    def test_add_grade(self):
        """Test adding a new grade to the repository."""
        grade = Grade(1234, 1, 9.5)
        self.repo.add_grade(1, 1234, 9.5)
        self.assertEqual(len(self.repo.list_all_grades()), 1, "Grade was not added.")


if __name__ == "__main__":
    unittest.main()
