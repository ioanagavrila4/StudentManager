class Grade(object):
    def __init__(self, assignment_id, student_id, grade_value):
        self.__id = assignment_id
        self.__student = student_id
        self._value = grade_value

    @property
    def id(self):
        return self.__id

    @property
    def student(self):
        return self.__student

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @student.setter
    def student(self, value):
        self.__student = value

    def __eq__(self, other):
        if not isinstance(other, Grade):
            return False
        return (self.student == other.student and
                self.id == other.id and
                self.value == other.value)

    def __str__(self):
        return f"{self.id} - {self.student} - {self.value} "

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    c1 = Grade(1, 2, 7)
    c2 = Grade(1, 2, 7)


