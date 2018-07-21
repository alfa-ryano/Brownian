def fn(v, lst=[]):
    lst.insert(0,v)
    print(lst)

fn([20])
fn(23)
fn(16, [1, 2])
fn([10], [3, 4])

def int2base(value, base):
    output = ""
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while value >= 1:
        if value < base:
            output = chars[value] + output
            break
        remaining = value % base
        value = value / base
        output = chars[remaining] + output

    return output

print int2base(10, 16)


def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    elif n > 1:
        return fibonacci(n - 1) + fibonacci(n - 2)
    else:
        return 0


even_count = 0
total = 0
n = 0
while even_count < 2:
    fib_number = fibonacci(n)
    if fib_number % 2 == 0:
        print even_count + 1, ":", fib_number
        even_count += 1
        total += fib_number
    n += 1

print total


def builtin_sort_two_arrays(array_a, array_b):
    return sorted(array_a + array_b)


def diy_sort_two_arrays(array_a, array_b):
    for element_a in array_a:

        i = 0
        found_pos = False
        while i < len(array_b):
            element_b = array_b[i]
            if element_a <= element_b:
                array_b.insert(i, element_a)
                found_pos = True
                break
            i += 1

        if found_pos == False:
            array_b.append(element_a)

    return array_b


a = [1, 5, 9]
b = [2, 4, 7]
print builtin_sort_two_arrays(a, b)
print diy_sort_two_arrays(a, b)