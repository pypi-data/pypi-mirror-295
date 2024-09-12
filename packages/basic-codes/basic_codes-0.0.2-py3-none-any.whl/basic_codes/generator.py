def genrator():
    one_to_five = [x for x in range(3)]
    for i in one_to_five:
        yield i

iterable = iter(genrator())
# print(next(iterable))
# print(next(iterable))
# print(next(iterable))

'''
Generator expression
'''
gen_expression = (x*x for x in range(1,6))

for num in gen_expression:
    print(num)

line = ('Helloworl: {}'.format('mR rakuh'),)
print(type(line))