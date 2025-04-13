import sys
import math
from fractions import Fraction
from decimal import Decimal
import re
from functools import singledispatchmethod
class Luythua:
    def __init__(self, data = None):
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
        print(f'({self.a}^{self.b})^({self.c}^{self.d})')
    @process.register
    def _2(self, l1: Fraction, l2 : Fraction):
        self.a, self.b = l1.numerator, l1.denominator
        self.c, self.d = l2.numerator, l2.denominator
        print(f'({self.a}^{self.b})^({self.c}^{self.d})')
    @process.register
    def _3(self, l : None):
        self.a, self.b, self.c, self.d = 0, 1, 1, 1
        print(f'({self.a}^{self.b})^({self.c}^{self.d})')
    @process.register
    def _4(self, l : Decimal):
        self.b = self.c = self.d = 1
        self.a = l
        print(f'({self.a}^{self.b})^({self.c}^{self.d})')
# Luythua(Decimal(0.1))