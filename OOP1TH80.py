from fractions import Fraction
import math, copy
import sys


class LuyThua:
    def __init__(self, input):
        x, y, z, t = self.extract_values(input)
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.indeterminate = False
        self.special_case = math.inf
        self.fraction1 = Fraction(1, 1)
        self.fraction2 = Fraction(1, 1)
        self.output = (0, 0, 0, 0)

    def extract_values(self, fraction_string):
        parts = fraction_string.split()  # Split into ["x/y", "z/t"]
        x, y = map(int, parts[0].split('/'))  # Split "x/y" into x, y
        z, t = map(int, parts[1].split('/'))  # Split "z/t" into z, t
        return x, y, z, t

    def initialize_fractions(self):
        self.fraction1 = Fraction(self.x, self.y)
        self.fraction2 = Fraction(self.z, self.t)
        self.x = self.fraction1.numerator
        self.y = self.fraction1.denominator
        self.z = self.fraction2.numerator
        self.t = self.fraction2.denominator

    def check_indeterminate(self):
        if self.y == 0 or self.t == 0:
            self.indeterminate = True
            return
        self.fraction1 = Fraction(self.x, self.y)
        self.fraction2 = Fraction(self.z, self.t)
        if self.fraction1 == 0 and self.fraction2 <= 0:
            self.indeterminate = True
        if self.fraction1 < 0 and self.fraction2.denominator % 2 == 0:
            self.indeterminate = True

    def check_special_case(self):
        case = self.fraction1 ** self.fraction2
        if case == 1 or case == 0 or case == -1:
            self.special_case = case

    def __get_len__(self, f = None):
        if f is None or len(f) < 4:
            return len(f"({self.x}/{self.y})^({self.z}/{self.t})")
        else:
            return len(f"({f[0]}/{f[1]})^({f[2]}/{f[3]})")

    def check_increase_exponent(self):
        f = [self.x, self.y, self.z, self.t] # 0 1 2 3
        count = 1
        len_str = self.__get_len__(f)
        max = [copy.deepcopy([f, len_str])]
        for _ in range(1000):
            count += 1
            f[2] = self.z*count
            f[0] = self.x**(1/count)
            f[1] = self.y**(1/count)
            f[3] = self.t
            if isinstance(f[0], complex) or isinstance(f[1], complex):
                continue
            if f[0] != int(f[0]) or f[1] != int(f[1]):
                continue
            f[0], f[1] = int(f[0]), int(f[1]) # Make them int again
            # # #
            temp_f1 = Fraction(f[0], f[1])
            temp_f2 = Fraction(f[2], f[3])
            f[0] = temp_f1.numerator
            f[1] = temp_f1.denominator
            f[2] = temp_f2.numerator
            f[3] = temp_f2.denominator
            # # #
            max.append(copy.deepcopy([f, self.__get_len__(f)]))
        min_value = min(x[1] for x in max)
        min_options = [x for x in max if x[1] == min_value]
        min_value_2 = min(min_options, key=lambda x:x[0])
        return min_value_2

    def check_decrease_exponent(self): # Copy of check_increase_exponent, similar logic
        f = [self.x, self.y, self.z, self.t] # 0 1 2 3
        count = 1
        len_str = self.__get_len__(f)
        max = [copy.deepcopy([f, len_str])]
        for _ in range(1000):
            count += 1
            f[2] = self.z/count
            f[0] = self.x**(count)
            f[1] = self.y**(count)
            f[3] = self.t
            if isinstance(f[2], complex):
                continue
            if f[2] != int(f[2]):
                continue
            f[2] = int(f[2]) # Make them int again
            # # #
            temp_f1 = Fraction(f[0], f[1])
            temp_f2 = Fraction(f[2], f[3])
            f[0] = temp_f1.numerator
            f[1] = temp_f1.denominator
            f[2] = temp_f2.numerator
            f[3] = temp_f2.denominator
            # # #
            max.append(copy.deepcopy([f, self.__get_len__(f)]))
        min_value = min(x[1] for x in max)
        min_options = [x for x in max if x[1] == min_value]
        min_value_2 = min(min_options, key=lambda x:x[0])
        return min_value_2

    def reduce(self):
        self.check_indeterminate()
        if self.indeterminate:
            return f"({self.x}/{self.y})^({self.z}/{self.t})"
        # # #
        self.initialize_fractions()
        self.check_special_case()
        if self.special_case == 0:
            return "(0/1)^(1/1)"
        if self.special_case == 1:
            return "(1/1)^(0/1)"
        if self.special_case == -1:
            return "(-9/9)^(1/1)"
        # # #
        self.initialize_fractions()
        if self.fraction2 < 0:
            self.fraction2 *= -1
            self.z = self.z*-1 if self.z < 0 else self.z
            self.t = self.t*-1 if self.z < 0 else self.t
            self.x, self.y = self.y, self.x
            self.fraction1 = Fraction(self.x, self.y)
        if self.z % 2 == 0 and self.fraction1 < 0:
            self.x *= -1
            self.initialize_fractions()
        increased = self.check_increase_exponent()
        decreased = self.check_decrease_exponent()
        get_min = increased
        if increased[1] > decreased[1]:
            get_min = decreased
        elif increased[1] == decreased[1]:
            if increased[0] > decreased[0]: get_min = decreased
        f = get_min[0]
        return f"({f[0]}/{f[1]})^({f[2]}/{f[3]})"

    def to_string(self):
        # This method exists merely because I don't wanna name reduce as to_string.
        return self.reduce()


# a = input()
# print(LuyThua(a).to_string())

def main():
    for l in sys.stdin.read().split('\n'):
        if l.strip():
            print(LuyThua(l.strip()).to_string())

if __name__ == "__main__":
    main()
