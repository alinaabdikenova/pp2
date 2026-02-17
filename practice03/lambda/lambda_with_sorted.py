#1
numbers = [5, 2, 9, 1]
desc = sorted(numbers, key=lambda x: -x)
print(desc)  # [9, 5, 2, 1]

#2
words = ["apple", "kiwi", "banana"]
by_length = sorted(words, key=lambda x: len(x))
print(by_length)  # ['kiwi', 'apple', 'banana']

#3
pairs = [(1, 3), (2, 1), (4, 2)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)  # [(2,1),(4,2),(1,3)]

#4
words = ["banana", "Apple", "cherry"]
sorted_words = sorted(words, key=lambda x: x.lower())
print(sorted_words)  # ['Apple', 'banana', 'cherry']
