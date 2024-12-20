class StudentNotFoundError(Exception):
    """Raised when a student is not found in the repository."""
    pass


class DuplicateStudentError(Exception):
    """Raised when attempting to add a student with a duplicate ID."""
    pass


class InvalidStudentUpdateError(Exception):
    """Raised when an invalid update is attempted on a student."""
    pass

class GradeAlreadyExistsError(Exception):
    """Raised when attempting to set a grade that already exists for a student and assignment."""
    pass


class InvalidGradeValueError(Exception):
    """Raised when an invalid grade value is provided."""
    pass


class GradeNotFoundError(Exception):
    """Raised when a specific grade entry is not found."""
    pass

class AssignmentAlreadyExistsError(Exception):
    """Raised when trying to add an assignment that already exists."""
    pass


class AssignmentNotFoundError(Exception):
    """Raised when an assignment is not found."""
    pass


class InvalidStudentError(Exception):
    """Raised when attempting to assign an assignment to a non-existent student."""
    pass


class InvalidGroupError(Exception):
    """Raised when attempting to assign an assignment to a non-existent group."""
    pass
