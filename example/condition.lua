num = 42
t = nil
flag = true

if num > 40 then
    num = 32
    print("true 0")
else
    print("false 0")
end

if t then
    print("true 1")
else
    print("false 1")
end

if flag then
    if t then
        print("true 2")
    else
        print("false 2")
    end
end

if flag and num then
    print("true 3")
end

if not flag then
    print("false 4")
end

if "" then
    print("string true")
end
