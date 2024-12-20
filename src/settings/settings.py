import configparser
import os
class Settings:
    def __init__(self, filename="settings.properties"):
        self.config = configparser.ConfigParser()

        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")  # Debug print the cwd

        file_path = os.path.join(cwd, filename)
        print(f"Loading settings from: {file_path}")  # Debug print the file path

        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
        else:
            # Read the settings file
            self.config.read(file_path)

            # Debugging: Print the content of the settings file
            print(f"Debug: Sections in the settings file: {self.config.sections()}")
            print(f"Debug: Settings content: {dict(self.config.items('DEFAULT'))}")

    def get_repository_type(self):
        return self.config.get('DEFAULT', 'repository', fallback='')

    def get_file_for_students(self):
        return self.config.get('DEFAULT', 'students', fallback='')

    def get_file_for_assignments(self):
        return self.config.get('DEFAULT', 'assignments', fallback='')

    def get_file_for_grades(self):
        return self.config.get('DEFAULT', 'grades', fallback='')

    def save_repositories(self, student_repo, assignment_repo, grade_repo):
        """
        Saves repositories based on the repository type.
        If the repository type is 'binaryfiles' or 'textfiles', the save logic is executed.
        """
        repository_type = self.get_repository_type()

        if repository_type == "binaryfiles" or repository_type == "textfiles":
            # If the repositories have explicit save methods
            if hasattr(student_repo, "_save_students"):
                student_repo._save_students()
            if hasattr(assignment_repo, "_save_assignments"):
                assignment_repo._save_assignments()
            if hasattr(grade_repo, "_save_grades"):
                grade_repo._save_grades()
        else:
            print("No save required for in-memory repository.")
