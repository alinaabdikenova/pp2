# parent class
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname


# child class using super()
class Student(Person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)


s = Student("Anna", "Smith")
print(s.firstname, s.lastname)