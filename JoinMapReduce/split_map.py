import sys

for line in sys.stdin:
    l = line.split()
    a = []
    c = []
    b = l[0]
    i = 1
    while i < len(l):
        if l[i] is 'a':
            a.append(l[i+1])
            i += 1
        else:
            c.append(l[i])
        i += 1

    for i in a:
        for j in c:
            print i + '\t' + b + '\t' + j

