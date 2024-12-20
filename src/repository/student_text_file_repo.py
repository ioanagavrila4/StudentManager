from src.domain.student import Student
from src.repository.memory_student import StudentRepository


class StudentTextFileRepository(StudentRepository):
    def __init__(self, filename):
        super().__init__()
        self.__fileName = filename
        self.__load_file()

    def __load_file(self):
        """
        Load students from a text file.
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
            new_student = Student(
                current_line[1].strip(),  # Name
                int(current_line[0].strip()),  # ID
                int(current_line[2].strip())   # Group
            )
            self._students[new_student.id] = new_student

    def __save_file(self):
        """
        Save all students to a text file.
        """
        with open(self.__fileName, "wt") as fout:
            for student in self._students.values():
                student_string = f"{student.id},{student.name},{student.group}\n"
                fout.write(student_string)

    def add_student(self, student):
        """
        Add a student to the repository and save to file.
        """
        super().add_student(student)
        self.__save_file()

    def remove_student(self, student_id, grade_repo):
        """
        Remove a student by ID and save changes to file.
        """
        super().remove_student(student_id, grade_repo)
        self.__save_file()

    def update_student(self, student_id, new_name=None, new_group=None):
        """
        Update a student's details and save changes to file.
        """
        updated_student = super().update_student(student_id, new_name, new_group)
        self.__save_file()
        return updated_student
