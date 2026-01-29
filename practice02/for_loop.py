#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#2
for x in "banana":
  print(x)

#3
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#4
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#5
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#6
for x in range(6):
  print(x)
