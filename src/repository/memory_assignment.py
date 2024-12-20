class AssignmentRepository:
    def __init__(self):
        # Store assignments in a dictionary
        self.assignments = {}

    def add_assignment(self, assignment):
        if assignment.id in self.assignments:
            pass
        self.assignments[assignment.id] = assignment
    def get(self, id):
        if id not in self.assignments:
            raise ValueError(f"Assignment {id} does not exist.")
        return self.assignments.get(id)
    def remove_assignment(self, assignment_id, grade_repo):
        if assignment_id not in self.assignments:
            raise ValueError(f"Assignment {assignment_id} does not exist.")
        grade_repo.remove_grades_for_assignment(assignment_id)
        del self.assignments[assignment_id]

    def update_assignment(self, assignment):
        if assignment.id not in self.assignments:
            pass
        self.assignments[assignment.id] = assignment
    def give_assignment_to_student(self, assignment_id, student_id, grade_repo):
        if assignment_id not in self.assignments:
            raise ValueError(f"Assignment {assignment_id} does not exist.")
        grade_repo.add_grade(student_id, assignment_id, grade_value=None)

    def give_assignment_to_group(self, assignment_id, group_id, student_repo, grade_repo):
        if assignment_id not in self.assignments:
            raise ValueError(f"Assignment {assignment_id} does not exist.")

        students_in_group = [student for student in student_repo.list_all() if student.group == group_id]
        if not students_in_group:
            raise ValueError(f"Group {group_id} does not exist or has no students.")

        for student in students_in_group:
            self.give_assignment_to_student(assignment_id, student.id, grade_repo)

    # New method to list all assignments
    def list_assignments(self):
        return list(self.assignments.values())

    def get_deadline_for_assignment(self, assignment_id):
        assignment = self.get(assignment_id)
        return assignment.deadline

    def get_ungraded_assignments_for_student(self, student_id, grade_repo):
        # Get all assignments assigned to the student
        all_assignments = grade_repo.get_assignments_for_student(student_id)

        # Filter out assignments that are already graded
        ungraded_assignments = [
            assignment_id for assignment_id in all_assignments
            if grade_repo.get_grade_for_assig(student_id, assignment_id) is None
        ]
        return ungraded_assignments