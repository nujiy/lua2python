num = 42
factor = 2
flag = true
s = 'walternate'  -- Immutable strings like Python.
t = nil

-- i = 12 single comment

----------------------------------------------------
-- Variables and flow control.
----------------------------------------------------

--[[
multi-line comment.
--]]

print(num)
num = num * factor
print(num)
num = num - 1
print(num)
num = num + 1

print(num, flag, s, t)
print 'Hello world!'
