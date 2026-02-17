# parent class
class Person:
    def printinfo(self):
        print("This is a person")


# child class overrides method
class Student(Person):
    def printinfo(self):
        print("This is a student")


p = Person()
s = Student()

p.printinfo()  # this is a person
s.printinfo()  # this is a student
