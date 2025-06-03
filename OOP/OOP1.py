import math
class point:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y
class triangle:
    def __init__(self, A : point, B : point, C : point):
        self.A = A
        self.B = B
        self.C = C
    def area(self):
        AB = math.sqrt((self.A.x - self.B.x)**2 + (self.A.y - self.B.y)**2)
        BC = math.sqrt((self.B.x - self.C.x)**2 + (self.B.y - self.C.y)**2)
        AC = math.sqrt((self.A.x - self.C.x)**2 + (self.A.y - self.C.y)**2)
        p = (AB + AC + BC) / 2
        return math.sqrt(p * (p - AB) * (p - AC) * (p - BC))
class quadrileteral:
    def __init__(self, A : point, B : point, C : point, D : point):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
    def area(self):
        return triangle(self.A, self.B, self.C).area() + triangle(self.D, self.A, self.C).area() 
