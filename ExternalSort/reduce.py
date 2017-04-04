import sys

word, count = sys.stdin.readline().split("\t")
count = int(count)
for line in sys.stdin:
    count += int(line.split("\t")[1])
print(word + "\t" + str(count))
