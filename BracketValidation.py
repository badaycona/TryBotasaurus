def main(s : str) -> bool:
    stack =list(s)
    res = ''
    for i in range(len(stack)):
        res += stack.pop()
    return res
s = str(input())
print(main(s))