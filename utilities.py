from math import sqrt

def inv_sqrt(x:int) -> int:
    if x == 0:
        raise NotImplementedError("invalid number")
    return x ** -0.5

class Vec2:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y 
    def __repr__(self) -> str:
        return "x: "+ str(self.x) + " y: " + str(self.y)

    def normalized(self):
        if (self.x*self.x) + (self.y*self.y) == 0:
            return Vec2(0,0)
        invsqrt = inv_sqrt((self.x*self.x) + (self.y*self.y))
        x = self.x * invsqrt
        y = self.y * invsqrt
        return Vec2(x, y)
    
    def magnitude(self):
        return sqrt(self.x*self.x + self.y*self.y)
    
    @classmethod
    def Distance(self, vecA, vecB):
        return ((vecB.x - vecA.x)*(vecB.x - vecA.x) + (vecB.y - vecA.y)*(vecB.y - vecA.y )) ** 0.5