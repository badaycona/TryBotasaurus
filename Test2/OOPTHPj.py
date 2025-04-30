from fractions import Fraction
from decimal import Decimal
class vector_3d:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    def __add__(self, other):
        return vector_3d(self._x + other._x, self._y + other._y, self._z + other._z)
    def __sub__(self, other):
        return vector_3d(self._x - other._x, self._y - other._y, self._z - other._z)
    def __neg__(self):
        return vector_3d(-self._x, -self._y, -self._z)
    def __str__(self):
        return f'({self._x}, {self._y}, {self._z})'
    def __mul__(self, other): 
        if isinstance(other, int):
            return vector_3d(self._x * other, self._y * other, self._z * other)
        elif isinstance(other, float):
            return vector_3d(self._x * other, self._y * other, self._z * other)
        elif isinstance(other, Fraction):
            a = other.numerator
            b = other.denominator
            x = Fraction(self._x * a, b)
            y = Fraction(self._y * a, b)
            z = Fraction(self._z * a, b)
            return vector_3d(x, y, z)
        return vector_3d(self._x * other, self._y * other, self._z * other)
    def __rmul__(self, other): 
        return self.__mul__(other)
    def __xor__(self, other):
        return vector_3d(self._y * other._z - self._z * other._y, self._z * other._x - self._x * other._z, self._x * other._y - self._y * other._x) 
    def __getattr__(self, other):
        k = eval(other)
        if isinstance(k, vector_3d):
            return self._x * k._x + self._y * k._y + self._z * k._z
        else:
            return self
    def x(self, x):
        self._x = x
    def y(self, y):
        self._y = y
    def z(self, z):
        self._z =z
a = vector_3d(1, 2, 3)
b = vector_3d(3, 2, 1)
# print(a + b)
# print(a - b)
# print(a ^ b)
# print(- a)
print(3 * a)
print(0.3 * a)
print(Fraction(2,5) * a)
print(Fraction(2,5))
# print(a.b)
# print(a.x(10))
# print(a.y(10))
# print(a.z(10))
# print(a)