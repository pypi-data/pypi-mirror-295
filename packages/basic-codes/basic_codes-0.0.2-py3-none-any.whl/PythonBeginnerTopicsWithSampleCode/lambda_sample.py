def add(a,b):
    print('Immediate action taken')
    return a + b


print((lambda a,b:a+b )(2,3))