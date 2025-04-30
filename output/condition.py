

def lua_truthy(value):
    return ((value is not None) and (value is not False))
num = 42
t = None
flag = True
if lua_truthy((num > 40)):
    num = 32
    print('true 0')
else:
    print('false 0')
if lua_truthy(t):
    print('true 1')
else:
    print('false 1')
if lua_truthy(flag):
    if lua_truthy(t):
        print('true 2')
    else:
        print('false 2')
if lua_truthy((flag and num)):
    print('true 3')
if lua_truthy((not flag)):
    print('false 4')
if lua_truthy(''):
    print('string true')
