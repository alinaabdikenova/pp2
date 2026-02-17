#1
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)


#2
def full_name(first, last):
    return f"{first} {last}"

print(full_name("Alya", "Smith"))


#3
def get_greeting():
  return "Hello from a function"

print(get_greeting())


#4:
def min_max(numbers):
    return min(numbers), max(numbers)

print(min_max([3, 7, 1, 9]))
