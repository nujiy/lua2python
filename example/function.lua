function bar(a, b)
    print(a)
    print(a, b)
    a = 1
    return (a + 1)
end

num = bar(1, true)

print(num)
