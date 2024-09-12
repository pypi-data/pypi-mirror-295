class NumberGroup:
    def __init__(self,x:int,y:int) -> None:
        self.x,self.y = x,y
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __repr__(self) -> str:
        return f"NumberGroup({self.x},{self.y})"
    
    def __add__(self, other: object)->int:
        return (self.x+other.x,self.y+other.y)
    
    def __eq__(self, other: object) -> bool:
        return True if self.x==other.x and other.y==self.y else False

        

G1 = NumberGroup(1,3)
G2 = NumberGroup(3,1)
print(G1+G2)
print(G1 == G2)
print(G1 == NumberGroup(1,3))