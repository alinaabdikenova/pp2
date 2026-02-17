#1
def greet():
    print("Hello, welcome to Python!")

greet()


#2
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alya")


#3
def add(a, b):
    return a + b

print(add(5, 3))


#4
def square(x):
    """Returns square of a number."""
    return x * x

def print_square(number):
    """Prints square of given number."""
    print(square(number))

print_square(4)
