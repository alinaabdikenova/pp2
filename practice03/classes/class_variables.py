#1
class Dog:
    species = "Woof"  # class variable
    
    def __init__(self, name):
        self.name = name  # instance variable

d1 = Dog("Buddy")
d2 = Dog("Max")
print(d1.species)  # Woof
print(d2.species)  # Woof


#2
d1.name = "Charlie"
print(d1.name)  # Charlie
print(d2.name)  # Max


#3: modify class variable
Dog.species = "Dog"
print(d1.species)  # Dog
print(d2.species)  # Dog



