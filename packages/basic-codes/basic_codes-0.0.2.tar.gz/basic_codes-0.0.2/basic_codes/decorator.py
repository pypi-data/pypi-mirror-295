'''
Example - 1
'''
import functools

# By using functools.wraps it will keep metadata of original function
def hello_decorator(func):
    @functools.wraps(func)
    def wrapper(*args):
        result = func(*args)
        result.append(9)
        return result
    return wrapper

def hello(num1):
    ''' it is an basic function just for learn decorators '''
    return [num1]


decorated = hello_decorator(hello)
print(hello(12))
print(decorated.__doc__)


'''
Example - 2
'''
def multiply_by_two(func):
    print('Multiplying')
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper

def divide_by_two(func):
    print('Deviding')
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        return result - 7
    return wrapper

@multiply_by_two
@divide_by_two
def add_numbers(a, b):
    return a + b

result = add_numbers(3, 4)
print(result)