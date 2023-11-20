# from time import strftime
#
# print(strftime("%I:%M:%S %p"))
# d = {"nm": "nage", "age": 35}
# n, a = d.values()
# print(n, a)

l1 = [3, 3, 6, 8, 7, 9, 2]

d = [{l1[i - 1]: l1[i]} for i in range(5)]

print(d)
