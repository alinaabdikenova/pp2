f = open("test.txt")
print(f.read())

with open("test.txt") as f:
  print(f.read(5))