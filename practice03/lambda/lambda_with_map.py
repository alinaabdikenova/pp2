#1
numbers = [1, 2, 3, 4]
doubled = list(map(lambda x: x*2, numbers))
print(doubled)  

#2
words = ["apple", "banana", "cherry"]
upper_words = list(map(lambda x: x.upper(), words))
print(upper_words)  # ['APPLE', 'BANANA', 'CHERRY']

#3
nums = [10, 20, 30]
add_five = list(map(lambda x: x+5, nums))
print(add_five)  # [15, 25, 35]

#4
squares = list(map(lambda x: x*x, [2,3,4]))
print(squares)  # [4, 9, 16]
