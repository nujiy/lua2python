

def bar(a, b):
    print(a)
    print(a, b)
    a = 1
    return (a + 1)
num = bar(1, True)
print(num)
