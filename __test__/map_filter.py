a = [1,2,3,4]
it = map(lambda x:print(x, end=' '),a)
next(it)
next(it)
next(it)
next(it)

# map
lst = list(map(lambda x:x**2,a))
print(lst)

# filter(조건문과 함께 특정 원소만 추출)
lst = list(filter(lambda x:x%2 == 0, a))
print(lst)





