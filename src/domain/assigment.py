import datetime
class Assignment(object):
    def __init__(self, assignment_id, description, deadline):
        self._id = assignment_id
        self._description = description
        self._deadline = deadline

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def deadline(self):
        return self._deadline

    @description.setter
    def description(self, description):
        self._description = description

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    def __eq__(self, z):
        # don't compare apples to oranges
        if type(z) != Assignment:
            return False
        # just look at the id field
        return self.id == z.id

    def __str__(self):
        return f"{self.id} - {self.description}- {self.deadline}"

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    c1 = Assignment(1000, "Proiect educatie tehnologica", datetime.datetime(2020, 5, 17))
    c2 = Assignment(1001, "Proiect lucru manual", datetime.datetime(2024, 4, 17))

    print({1000: c1, 1001: c2})