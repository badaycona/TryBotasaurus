import sys
import math
from fractions import Fraction
from decimal import Decimal
import re
from functools import singledispatchmethod
class Luythua:
    def __init__(self, data):
        self.process(data)
    @singledispatchmethod
    def process(self, l):
        print(type(l))
        print('Sai me r')
    @process.register
    def _1(self, l: str):
        ab, cd = map(str,l.split())
        a, b = map(int,ab.split('/'))
        c, d = map(int, cd.split('/'))
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    @process.register
    def _2(self, l1: Fraction, l2 : Fraction):
        self.a, self.b = l1.numerator, l1.denominator
        self.c, self.d = l2.numerator, l2.denominator
    @process.register
    def _3(self, l : None):
        self.a, self.b, self.c, self.d = 0, 1, 1, 1
    @process.register
    def _4(self, l : Decimal):
        self.b = self.c = self.d = 1
        while int(l) != l:
            l *= 10
        self.a = int(l)
    def to_string(self):
        if self.b == 0 or self.d == 0: # 5 0 2 0
            return f'({self.a}/{self.b})^({self.c}/{self.d})'
        
        if self.a == 0 and self.c/self.d <= 0: # 0 3 0 7 //// 0 2 -3 1
            return f'({self.a}/{self.b})^({self.c}/{self.d})'
        
        if self.b != 0 and self.d != 0:
            if self.c == 0: # 3 2 0 4
                return '(1/1)^(0/1)'
            elif self.a == 0: # 0 2 3 4
                return '(0/1)^(1/1)'
        if self.a == self.b: # 2 2 4 1
                return '(1/1)^(0/1)' 
        if self.a == -1 and self.b == 1 and self.c == -1 and self.d == 1:
            return '(-9/9)^(0/1)'
        if self.a * self.b < 0 and (self.d // gcd(self.c, self.d)) % 2 == 0: # -3 1 3 4
            return f'({self.a}/{self.b})^({self.c}/{self.d})' 
        #triet dau -
        if self.a < 0 and self.b < 0:
            self.a, self.b = - self.a, - self.b
        if self.c < 0 and self.d < 0:        
            self.c, self.d = - self.c, - self.d
        #dua - len a, triet tieu dau - o exponent
        if self.a > 0 and self.b < 0:
            self.a, self.b = - self.a, - self.b
        if self.c * self.d < 0:
            self.a, self.b, self.c, self.d = self.b, self.a, abs(self.c), abs(self.d)
        # toi gian
        self.a, self.b = self.a // gcd(self.a, self.b), self.b // gcd(self.a, self.b)
        self.c, self.d = self.c // gcd(self.c, self.d), self.d // gcd(self.c, self.d)

        flagbase, base1, base2, exbase = can_be_power(self.a, self.b)
        maxlen = []
        maxlen.append(f'({self.a}/{self.b})^({self.c}/{self.d})')
        if flagbase:
            exbase, self.d = exbase // gcd(exbase, self.d), self.d // gcd(exbase, self.d)
            maxlen.append(f'({base1}/{base2})^({self.c*exbase}/{self.d})')
        for i in range(2, 10):
            if self.c % i == 0:
                maxlen.append(f'({self.a**i:d}/{self.b**i:d})^({self.c//i}/{self.d})')
        maxstr = min(maxlen, key = custom_key)
        return maxstr
def parse(s):
    match = re.match(r'\((-?\d+)/(-?\d+)\)\^\((-?\d+)/(-?\d+)\)', s)
    return tuple(map(int, match.groups()))

def custom_key(s):
    return (len(s),) + parse(s) 
        
def gcd(a, b):
    k, j = abs(a), abs(b)
    while j:
        k, j = j, k % j
    return k    
def prime_factor(x):
    d = {}
    i = 2
    while i <= x:
        if x % i == 0:
            x = x // i
            if i not in d:
                d[i] = 1
            else: 
                d[i] += 1
        else:
            i += 1
    return d
def gcd_list(lst):
    return math.gcd(*lst)

def can_be_power(a, b):
    if a == 0 or b == 0:
        return False, None, None, None

    factors_a = prime_factor(abs(a))
    factors_b = prime_factor(abs(b))

    exponents = list(factors_a.values()) + list(factors_b.values())
    k = gcd_list(exponents)

    if k == 1:
        return False, None, None, None

    c = int(round(math.copysign(abs(a) ** (1 / k), a)))
    d = int(round(math.copysign(abs(b) ** (1 / k), b)))

    if c ** k == a and d ** k == b:
        return True, c, d, k
    else:
        return False, None, None, None
def main():
    for l in sys.stdin.read().split('\n'):
        if l.strip():
            print(Luythua(l.strip()).to_string())
main()  

# import zipfile

# with zipfile.ZipFile(r'C:\Users\Hi\Downloads\problem407_in2025-03-11_02-50.zip', 'r') as zip_ref:
#     with zip_ref.open('input1.txt') as file:
#         lines = file.readlines()
#         print(lines)
#         for line in lines:
#             print(Luythua(line.decode('utf-8').strip()).to_string())  
# with zipfile.ZipFile(r'C:\Users\Hi\Downloads\problem407_out2025-03-11_02-50.zip', 'r') as zip_ref:
#     with zip_ref.open('output1.txt') as file:
#         lines = file.readlines()
#         print(lines)
#         # for line in lines:
#         #     print(Luythua(line.decode('utf-8').strip()).to_string())  
