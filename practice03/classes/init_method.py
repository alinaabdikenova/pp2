
#1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alya", 20)
print(p.name, p.age)  # Alya 20


#2
class Car:
    def __init__(self, brand="Toyota", color="Red"):
        self.brand = brand
        self.color = color

c1 = Car()
c2 = Car("Honda", "Blue")
print(c1.brand, c1.color)  # Toyota Red
print(c2.brand, c2.color)  # Honda Blue


#3
class Team:
    def __init__(self, members):
        self.members = members

team = Team(["Alice", "Bob"])
print(team.members)  # ['Alice', 'Bob']



