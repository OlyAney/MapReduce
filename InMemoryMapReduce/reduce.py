import sys

word, count = sys.stdin.readline().split("\t")
count = int(count) #0 тут быть не должно, потому что первая строка уже считана
for line in sys.stdin:
    count += 1
print(word + "\t" + str(count))
