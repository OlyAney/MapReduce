import sys

word, count = sys.stdin.readline().split("\t")
count = int(count)
for line in sys.stdin:
    cur_word, cur_count = line.split("\t")
    cur_count = int(cur_count)
    if cur_word == word:
        count += cur_count
    else:
        print(word + "\t" + str(count))
        word = cur_word
        count = cur_count
print (word + "\t" + str(count))
