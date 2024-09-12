class Main:
    def __init__(self) -> None:
        print('Maveli vanne')

    def __first(self):
        print('Second declared')
    
    def get_first(sel):
        sel.__first()

class MainChild(Main):
    def __init__(self) -> None:
        print('Maveli poyee')
    def call_super_first(sel):
        super().__init__()

class MainGrandChild(Main):
    def __init__(self) -> None:
        print('Maveli Veendum Poye')

    def call_super_first(sel):
        sup = super()
        sup.super().__init__()

obj3 = MainGrandChild()
# obj3.call_super_first()

def return_list():
    res = [].append(3)
    res.append(2)
    return res

# print(return_list())