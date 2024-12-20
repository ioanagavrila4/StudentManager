class Student(object):
    def __init__(self, name, student_id, student_group, assign_list=None):
        self.__id = student_id
        self._name = name
        self.__group = student_group
        # Store assignments as tuples of (assignment_id, gr
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name:
            raise ValueError("Name cannot be empty.")
        self._name = new_name

    @property
    def group(self):
        return self.__group


    @group.setter
    def group(self, new_group):
        if new_group is None:
            raise ValueError("Group must be a valid integer.")
        self.__group = new_group

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.id == other.id

    def __str__(self):
        return f"{self.id} - {self.name} - {self.group}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.id)
