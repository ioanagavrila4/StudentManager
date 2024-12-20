class GradeRepository:
    def __init__(self):
        # Store grades as tuples: {(assignment_id, student_id): grade_value}
        self.grades = {}
        self.student_assignments = {}  # {student_id: [assignment_id, ...]}
    def add_grade(self, student_id, assignment_id, grade_value):
        # Add the grade for the student
        self.grades[(assignment_id, student_id)] = grade_value

        # Ensure assignment is tracked for the student
        if student_id not in self.student_assignments:
            self.student_assignments[student_id] = []
        if assignment_id not in self.student_assignments[student_id]:
            self.student_assignments[student_id].append(assignment_id)

    def update_grade(self, student_id, assignment_id, grade_value):
        if (assignment_id, student_id) not in self.grades:
            raise ValueError(f"No grade exists for student {student_id} on assignment {assignment_id}.")
        self.grades[(assignment_id, student_id)] = grade_value

    def get_grades_for_student(self, student_id):
        """
        Retrieve assignments and grades for a student.
        :param student_id: The ID of the student whose grades are to be retrieved.
        :return: A list of tuples, where each tuple contains (assignment_id, grade_value).
        """
        assignments_and_grades = []
        for (assignment_id, s_id), grade_value in self.grades.items():
            if s_id == student_id:
                # Append a tuple (assignment_id, grade_value) to the list
                assignments_and_grades.append((assignment_id, grade_value))
        return assignments_and_grades

    def get_assignments_for_student(self, student_id):
        """
        Retrieve all assignment IDs for a specific student.
        """
        assignments = set()  # Use a set to avoid duplicates
        for (assignment_id, s_id), _ in self.grades.items():
            if s_id == student_id:
                assignments.add(assignment_id)
        return list(assignments)  # Convert the set to a list

    def find_by_student_and_assignment(self, student_id, assignment_id):
        # Ensure we are checking for the correct key structure
        grade = self.grades.get((assignment_id, student_id))
        return grade

    def delete(self, student_id, assignment_id):
        # Check if the grade exists for the specific student and assignment
        grade = self.find_by_student_and_assignment(student_id, assignment_id)

        if grade is not None:
            # If grade exists, delete it from the grades dictionary
            del self.grades[(assignment_id, student_id)]
        else:
            raise ValueError(f"Grade for student {student_id} and assignment {assignment_id} not found.")

    def remove_grades_for_assignment(self, assignment_id):
        # Remove all grades for a specific assignment
        self.grades = {k: v for k, v in self.grades.items() if k[0] != assignment_id}

    def remove_grades_for_student(self, student_id):
        # Remove all grades for a specific student
        self.grades = {k: v for k, v in self.grades.items() if k[1] != student_id}

    def get_grade_for_assig(self, student_id, assignment_id):
        """
        Retrieve the grade for a specific student and assignment.
        """
        return self.grades.get((assignment_id, student_id), None)
