#1
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

#2: 
words = ["cat", "banana", "apple", "kiwi"]
long_words = list(filter(lambda x: len(x) > 5, words))
print(long_words)  # ['banana']

#3
nums = [5, 12, 7, 20]
gt_ten = list(filter(lambda x: x > 10, nums))
print(gt_ten)  # [12, 20]

#4
odds = list(filter(lambda x: x % 2 != 0, [1,2,3,4,5]))
print(odds)  # [1, 3, 5]
