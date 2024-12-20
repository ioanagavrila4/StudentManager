from faker import Faker
import random

from src.repository.memory_student import StudentRepository
from src.repository.memory_assignment import AssignmentRepository
from src.repository.memory_grade import GradeRepository
from src.services.student_service import StudentService
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.domain.student import Student
from src.domain.assigment import Assignment
from src.domain.grade import Grade
from src.services.undo_service import UndoService, Operation, FunctionCall
from src.settings.settings import Settings
from src.exceptions.exceptions import (
    StudentNotFoundError, AssignmentNotFoundError, AssignmentAlreadyExistsError,
    InvalidStudentError, DuplicateStudentError, InvalidStudentUpdateError,
    GradeAlreadyExistsError, GradeNotFoundError, InvalidGroupError, InvalidGradeValueError
)

fake = Faker()


# --- DATA GENERATORS ---
def generate_students(assignments, num_students=20):
    students = []
    for _ in range(num_students):
        student_id = random.randint(1000, 9999)
        name = fake.name()
        group = random.randint(900, 999)

        assigned_assignments = set(random.sample([a.id for a in assignments], k=random.randint(1, len(assignments)//2)))
        student = Student(name, student_id, group, assign_list=assigned_assignments)
        students.append(student)
    return students


def generate_assignments(num_assignments=20):
    assignments = []
    for _ in range(num_assignments):
        assignment_id = random.randint(1000, 9999)
        description = fake.sentence(nb_words=6)
        deadline = fake.date_this_decade()
        assignment = Assignment(assignment_id, description, deadline)
        assignments.append(assignment)
    return assignments


import random


import random

def generate_grades(student_repo, assignment_repo, grade_repo, num_grades=20):
    # Step 1: Assign all assignments to students
    for student in student_repo.list_all():
        for assignment in assignment_repo.list_assignments():
            # Check if the student already has the assignment linked, if not, assign it
            if assignment.id not in grade_repo.get_assignments_for_student(student.id):
                grade_repo.add_grade(student.id, assignment.id, None)
                print(f"Assigned Assignment {assignment.id} to Student {student.id} (No Grade Yet)")

    # Step 2: Generate grades for students and assignments
    for _ in range(num_grades):
        student = random.choice(student_repo.list_all())  # Randomly select a student
        assignment = random.choice(assignment_repo.list_assignments())  # Randomly select an assignment

        # Ensure the student is assigned to this assignment
        if assignment.id not in grade_repo.get_assignments_for_student(student.id):
            grade_repo.add_grade(student.id, assignment.id, None)
            print(f"Assigned Assignment {assignment.id} to Student {student.id} (No Grade Yet)")

        # Randomly decide whether to leave ungraded or assign a grade
        grade_value = random.randint(1, 10)  # Assign a grade between 1 and 10
        if random.random() < 0.3:  # 30% chance to leave as None
            grade_value = None

        # Update or set the grade
        try:
            grade_repo.update_grade(student.id, assignment.id, grade_value)
            print(f"Updated grade for Student {student.id}, Assignment {assignment.id}: {grade_value}")
        except ValueError as e:
            print(f"Could not update grade: {e}")

def view_assignments_and_grades(assignment_service, assignment_repo):
    student_id = int(input("Enter your student ID: "))
    assignments_and_grades = assignment_service.list_student_assignments(student_id)

    print(f"\nAssignments and Grades for Student ID {student_id}:")
    print(assignments_and_grades)

def view_grades(assignment_service, grade_repo:GradeRepository):
    student_id = int(input("Enter your student ID: "))
    grades_values = grade_repo.get_grades_for_student(student_id)

    print(f"\nAssignments and Grades for Student ID {student_id}:")
    print(grades_values)
import os

def choose_repository():
    settings = Settings("settings.properties")
    repository_type = settings.get_repository_type()
    undo_service = UndoService()
    if repository_type == "inmemory":
        student_repo = StudentRepository()
        assignment_repo = AssignmentRepository()
        grade_repo = GradeRepository()
    elif repository_type == "binaryfiles":
        from src.repository.student_binary_file_repo import StudentBinaryFileRepository
        from src.repository.assig_binary_file_repo import AssignmentBinaryFileRepository
        from src.repository.grade_binary_file_repo import GradeBinaryFileRepository

        student_repo = StudentBinaryFileRepository(settings.get_file_for_students())
        assignment_repo = AssignmentBinaryFileRepository(settings.get_file_for_assignments())
        grade_repo = GradeBinaryFileRepository(settings.get_file_for_grades())
    elif repository_type == "textfiles":
        from src.repository.student_text_file_repo import StudentTextFileRepository
        from src.repository.assignment_text_file_repo import AssignmentTextFileRepository
        from src.repository.grade_text_file_repo import GradeTextFileRepository

        student_repo = StudentTextFileRepository(settings.get_file_for_students())
        assignment_repo = AssignmentTextFileRepository(settings.get_file_for_assignments())
        grade_repo = GradeTextFileRepository(settings.get_file_for_grades())
    else:
        student_repo = StudentRepository()
        assignment_repo = AssignmentRepository()
        grade_repo = GradeRepository()

    # Populate repositories with initial data
    list_of_assignments = generate_assignments()
    for student in generate_students(list_of_assignments):
        student_repo.add_student(student)
    for assignment in list_of_assignments:
        assignment_repo.add_assignment(assignment)
    generate_grades(student_repo, assignment_repo, grade_repo)

    # Automatically save repositories if needed
    settings.save_repositories(student_repo, assignment_repo, grade_repo)

    return student_repo, assignment_repo, grade_repo


# --- MENU DISPLAY ---
def display_main_menu():
    print("\n--- Main Menu ---")
    print("1. Manage Students")
    print("2. Manage Assignments")
    print("3. Assign Assignments")
    print("4. Grade Students")
    print("5. View Student Assignments")  # New menu option
    print("6. Display student assignments+grades for them")
    print("7. All students who received a given assignment, ordered descending by grade")
    print("8. All students who are late in handing in at least one assignment. These are all the students who have an ungraded assignment for which the deadline has passed.")
    print("9. Students with the best school situation, sorted in descending order of the average grade received for all graded assignments.")
    print("10. EXIT ")


def validate_numeric_input(prompt, input_type=int):
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def manage_students(student_service, undo_service: UndoService):
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Update Student")
        print("4. List Students")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            student_id = validate_numeric_input("Enter student ID: ")
            group = validate_numeric_input("Enter student group: ")
            student = Student(name, student_id, group)

            # Add student
            student_service.add(student)

            # Record for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(student_service.remove, student_id),
                    redo_function=FunctionCall(student_service.add, student)
                )
            )
            print(f"Student {name} added.")
        elif choice == "2":
            student_id = validate_numeric_input("Enter student ID to remove: ")
            student = student_service.get(student_id)

            # Remove student
            student_service.remove(student_id)

            # Record for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(student_service.add, student),
                    redo_function=FunctionCall(student_service.remove, student_id)
                )
            )
            print(f"Student with ID {student_id} removed.")
        elif choice == "3":
            student_id = validate_numeric_input("Enter student ID to update: ")
            new_name = input("Enter new name (press enter to skip): ").strip()
            new_group = input("Enter new group (press enter to skip): ").strip()

            student = student_service.get(student_id)
            previous_data = {'name': student.name, 'group': student.group}

            # Update student
            student_service.update(student_id, new_name or None, new_group or None)

            # Record for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(
                        student_service.update,
                        student_id, previous_data['name'], previous_data['group']
                    ),
                    redo_function=FunctionCall(
                        student_service.update,
                        student_id, new_name or previous_data['name'], new_group or previous_data['group']
                    )
                )
            )
            print(f"Student with ID {student_id} updated.")

        elif choice == "4":
            students = student_service.list_all()
            for student in students:
                print(student)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

# Function to manage assignments
def manage_assignments(assignment_service, grade_repo, undo_service):
    while True:
        print("\n--- Assignment Management ---")
        print("1. Add Assignment")
        print("2. Remove Assignment")
        print("3. Update Assignment")
        print("4. List Assignments")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == "1":
            description = input("Enter assignment description: ").strip()
            deadline = input("Enter assignment deadline (YYYY-MM-DD): ").strip()
            assignment_id = validate_numeric_input("Enter assignment ID: ")
            assignment = Assignment(assignment_id, description, deadline)

            # Perform the action (e.g., adding an assignment)
            assignment_service.add_assignment(assignment)

            # Record the operation for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(
                        assignment_service.remove_assignment,
                        assignment_id
                    ),
                    redo_function=FunctionCall(
                        assignment_service.add_assignment,
                        assignment
                    )
                )
            )
            print(f"Assignment '{description}' added.")

        elif choice == "2":
            assignment_id = validate_numeric_input("Enter assignment ID to remove: ")
            assignment = assignment_service.get_assignment(assignment_id)

            # Remove assignment
            assignment_service.remove_assignment(assignment_id, grade_repo)

            # Record for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(assignment_service.add_assignment, assignment),
                    redo_function=FunctionCall(assignment_service.remove_assignment, assignment_id, grade_repo)
                )
            )
            print(f"Assignment with ID {assignment_id} removed.")

        elif choice == "3":
            assignment_id = validate_numeric_input("Enter assignment ID to update: ")
            new_description = input("Enter new description (press enter to skip): ").strip()
            new_deadline = input("Enter new deadline (press enter to skip): ").strip()

            assignment = assignment_service.get(assignment_id)
            previous_data = {'description': assignment.description, 'deadline': assignment.deadline}

            # Update assignment
            assignment_service.update_assignment(assignment_id, new_description or None, new_deadline or None)

            # Record for undo/redo
            undo_service.record(
                Operation(
                    undo_function=FunctionCall(
                        assignment_service.update_assignment,
                        assignment_id, previous_data['description'], previous_data['deadline']
                    ),
                    redo_function=FunctionCall(
                        assignment_service.update_assignment,
                        assignment_id, new_description or assignment.description, new_deadline or assignment.deadline
                    )
                )
            )
            print(f"Assignment with ID {assignment_id} updated.")

        elif choice == "4":
            assignments = assignment_service.list_all_assignments()
            if not assignments:
                print("No assignments found.")
            else:
                for assignment in assignments:
                    print(assignment)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


# Function to grade students
def grade_student(grade_service, student_repo, assignment_repo, assignment_service, undo_service):
    print("\n--- Grade a Student ---")
    student_id = validate_numeric_input("Enter student ID to grade: ")

    try:
        # Step 1: Get ungraded assignment IDs for the student
        ungraded_assignment_ids = grade_service.get_ungraded_assignments_for_student(student_id)

        if not ungraded_assignment_ids:
            print("No ungraded assignments for this student.")
            return

        print("Select assignment to grade:")

        # Step 2: Display ungraded assignments with details
        for idx, assignment_id in enumerate(ungraded_assignment_ids, start=1):
            assignment = assignment_repo.get(assignment_id)
            print(f"{idx}. Assignment ID: {assignment.id}, Description: {assignment.description}")

        choice = validate_numeric_input("Enter choice: ")
        if choice < 1 or choice > len(ungraded_assignment_ids):
            print("Invalid choice. Please select a valid assignment index.")
            return

        # Step 3: Retrieve the selected assignment ID
        selected_assignment_id = ungraded_assignment_ids[choice - 1]

        # Step 4: Validate and input grade
        grade_value = int(input("Please enter a grade value (1-10): "))
        if not (1 <= grade_value <= 10):
            print("Invalid grade. Please enter a value between 1 and 10.")
            return

        # Step 5: Grade the student
        grade_service.grade_student(student_id, selected_assignment_id, grade_value)
        print(f"Successfully graded student {student_id} for assignment {selected_assignment_id} with grade {grade_value}.")

        # Step 6: Record the action for undo functionality
        undo_service.record(
            Operation(
                undo_function=FunctionCall(grade_service.remove_grade, student_id, selected_assignment_id),
                redo_function=FunctionCall(grade_service.grade_student, student_id, selected_assignment_id, grade_value)
            )
        )

    except StudentNotFoundError:
        print("Error: Student not found.")
    except GradeAlreadyExistsError:
        print("Error: Grade for this assignment already exists.")
    except ValueError as e:
        print(f"Error: {e}")

def display_late_students_with_ungraded_assignments(grade_service):
    # Fetch late students who have ungraded assignments past their deadline
    late_students = grade_service.get_late_students_with_ungraded_assignments()

    # If there are no late students
    if not late_students:
        print("\nNo students are late in handing in any assignments.")
        return

    # Print the list of students who are late
    print("\nStudents who are late in handing in at least one assignment:")
    for student in late_students:
        print(f"Student ID: {student.id}, Name: {student.name}")


def display_students_with_best_grades(grade_service):
    print("\n--- Students with the Best School Situation ---")

    students_with_grades = grade_service.get_students_with_best_grades()

    if not students_with_grades:
        print("No students with grades available.")
        return

    print(f"{'Student ID':<12}{'Name':<20}{'Average Grade'}")
    print("-" * 45)
    for student, avg_grade in students_with_grades:
        print(f"{student.id:<12}{student.name:<20}{avg_grade:.2f}")


def assign_to_students(assignment_service: AssignmentService, student_repo: StudentRepository):
    print("\n--- Assign an Assignment ---")
    print("1. Assign to a single student")
    print("2. Assign to a group")
    choice = input("Enter choice: ")

    assignment_id = int(input("Enter assignment ID to assign: "))

    if choice == "1":
        student_id = int(input("Enter student ID to assign the assignment to: "))
        try:
            assignment_service.assign_to_students(assignment_id, [student_id])
            print(f"Assignment {assignment_id} successfully assigned to student {student_id}.")
        except ValueError as e:
            print(e)

    elif choice == "2":
        group = int(input("Enter group number to assign to: "))
        # Fetch students in the group
        students_in_group = [
            student.id for student in student_repo.list_all() if student.group == group
        ]
        if not students_in_group:
            print(f"No students found in group {group}.")
            return

        try:
            assignment_service.assign_to_students(assignment_id, students_in_group)
            print(f"Assignment {assignment_id} successfully assigned to group {group}.")
        except ValueError as e:
            print(e)

    else:
        print("Invalid choice. Please try again.")


def main():
    student_repo, assignment_repo, grade_repo = choose_repository()
    undo_service = UndoService()
    student_service = StudentService(student_repo, grade_repo, undo_service)
    assignment_service = AssignmentService(assignment_repo, student_repo, undo_service)
    grade_service = GradeService(grade_repo, student_repo, assignment_repo, undo_service)

    actions_history = []  # Stores actions for undo
    redo_history = []     # Stores undone actions for redo

    while True:
        display_main_menu()
        print("0. Undo Last Action")
        print("11. Redo Last Action")
        choice = input("Enter choice: ")

        if choice == "1":
            manage_students(student_service, undo_service)
            redo_history.clear()  # Clear redo history when a new action is taken
        elif choice == "2":
            manage_assignments(assignment_service, grade_repo, undo_service)
            redo_history.clear()  # Clear redo history when a new action is taken
        elif choice == "3":
            assign_to_students(assignment_service, student_repo)
            redo_history.clear()  # Clear redo history when a new action is taken
        elif choice == "4":
            grade_student(grade_service, student_repo, assignment_repo, assignment_service, undo_service)
            redo_history.clear()  # Clear redo history when a new action is taken
        elif choice == "6":
            view_grades(assignment_service, grade_repo)
        elif choice == "7":
            assignment_id = int(input("Enter assignment ID: "))
            results = grade_service.get_students_with_assignment_ordered_by_grade(assignment_id)
            print("\nStudents with Assignment ID", assignment_id)
            for student, grade in results:
                print(f"Student ID: {student.id}, Name: {student.name}, Grade: {grade}")
        elif choice == "8":
            display_late_students_with_ungraded_assignments(grade_service)
        elif choice == "9":
            display_students_with_best_grades(grade_service)
        elif choice == "10":
            print("Goodbye!")
            break
        elif choice == "0":
            try:
                undo_service.undo()
                print("Last action undone.")
            except ValueError as e:
                print(e)
        elif choice == "11":
            try:
                undo_service.redo()
                print("Last undone action redone.")
            except ValueError as e:
                print(e)
        else:
            print("Invalid choice. Try again.")



if __name__ == "__main__":
    main()


