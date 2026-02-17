#1
class Dog:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print(f"{self.name} says woof!")

d = Dog("Sobaka")
d.greet()  # Sobaka says woof!


#2
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def get_info(self):
    return f"{self.name} is {self.age} years old"

p1 = Person("Tobias", 28)
print(p1.get_info())


#3  the __str__() method:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def __str__(self):
    return f"{self.name} ({self.age})"

p1 = Person("Tobias", 36)
print(p1)
