import sys

word, count = sys.stdin.readline().split("\t")
count = int(count) # ведь правда же здесь должен быть 0 ?
for line in sys.stdin:
    count += 1
print(word + "\t" + str(count))
