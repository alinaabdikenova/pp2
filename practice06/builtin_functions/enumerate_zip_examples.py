y = ('car', 'plane', 'maserati')
y2 = enumerate(y)

names = ["a", "b", "c"]
scores = [90, 80, 70]

for i, name in enumerate(names):
    print(i, name)

for n, s in zip(names, scores):
    print(n, s)