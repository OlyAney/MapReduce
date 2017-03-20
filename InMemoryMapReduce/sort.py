import sys

data = []
for line in sys.stdin:
    data.append((line.split(" "))[0])
data.sort()
for s in data:
    print str(s) + "\t1".strip('\n')