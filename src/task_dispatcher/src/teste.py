x = []

x.append(('t1',100))

x.append(('t2',20))

print(x)

x.sort(key=lambda tup: tup[1], reverse=True)

print(x)

print(x.pop())

print(x)