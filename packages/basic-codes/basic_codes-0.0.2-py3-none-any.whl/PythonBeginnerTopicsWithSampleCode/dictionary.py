def my_func(**kwargs)-> dict:
    '''
    Basically takes keyword arguments and 
    return same dictinay after swapping the keys and values
    '''
    return {v:k for k,v in kwargs.items()}

print(my_func(hello=90))