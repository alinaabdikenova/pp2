#1
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(sum_all(1, 2, 3, 4))


#2
def print_items(*items):
    for item in items:
        print(item)

print_items("apple", "banana", "cherry")


#3
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")


#4
def example_function(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

example_function(1, 2, 3, name="Alya", grade="A")
