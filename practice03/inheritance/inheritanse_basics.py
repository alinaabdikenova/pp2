#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#object from parent class
x = Person("John", "Doe")
x.printname()

#child class
class Student(Person):
  pass

y = Student("Mike", "Olsen")
y.printname() 


