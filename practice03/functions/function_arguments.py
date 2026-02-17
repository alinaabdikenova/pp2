#1
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()
greet("Alya")


#2
def multiply(a, b, c):
    return a * b * c

print(multiply(2, 3, 4))


#3
def student_info(name, age):
    print(f"Name: {name}, Age: {age}")

student_info(age=20, name="Alya")


#4
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)