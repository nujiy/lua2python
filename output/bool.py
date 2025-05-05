

def lua_truthy(value):
    return ((value is not None) and (value is not False))
val = True
aBoolValue = True
if lua_truthy((not aBoolValue)):
    print('false')
if lua_truthy(aBoolValue):
    print('true')
v = (not aBoolValue)
print(v)
