class MyClass:
    def __init__(self,a,b) -> None:
        self.a = a
        self.b = b
        
    
    def __repr__(self) -> str:
        return f'iam {self.a},{self.b} (repr) '
    
    def __str__(self) -> str:
        return f'iam {self.a},{self.b}'
    
    
obj1 = MyClass(10,20)
obj2 = MyClass(11,22)
print('hello'.__delattr__('h'))
print(obj1)
print(obj2)