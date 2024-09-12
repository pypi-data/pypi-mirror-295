'''
MAP
'''
#1 
res  = list(map(str.upper,['a','b']))

#2
areas = [1.234,5.3058, 8.3901,3.9428,7.1638]

def sub_with_n(digit,n) -> int:
    return round(digit - n)

# print(list(map(sub_with_n,areas,range(1,6))))
# print(list(map(round,areas,range(1,6))))

#3 custom zip using map,lambda
nums = [1,2,3,4,5]
chars = ['a','b','c','d','e']

combination = tuple(map(lambda x,y:(x,y),chars,nums))
# print(combination)


'''
Filter
'''
caps_only = list(filter(str.isupper,'hjvjVJHVjhvJHVhuhisujVjhvJHvjHVjHVhjvG'))
# print(caps_only)

'filter palindrome words'
palims = ['abcba','engne','malayalam','sdffdd','poooiop']
palims_only = list(filter(lambda x: x==x[::-1],palims))
# print(palims_only)


'''
Reduce
'''
from functools import reduce
import time
def custom_sum(first,second):
        return first+second

numbers = [1,45,2,56,24,8,35,13]

total_sum = reduce(custom_sum,numbers)
print(total_sum)