import sys

a = b = c = ""
first_line = sys.stdin.readline()
temp_b = first_line.split()[0]
try:
    a += '\ta\t' + first_line.split()[2]   #if the value is "A" type, then .split() returns a list of 3 elements
except:
    c += '\t' + first_line.split()[1]

#first line already read
for line in sys.stdin:
    b = line.split()[0]
    if b != temp_b:
        print temp_b, a, c
        temp_b = b
        a = ''
        c = ''
    try:
        a += '\ta\t' + line.split()[2]
    except:
        c += '\t' + line.split()[1]
print b, a, c