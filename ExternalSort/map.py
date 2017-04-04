import sys

for line in sys.stdin:
    # for i in range(1, len(sys.argv)):      //to test multiple arguments for map script
    #    print sys.argv[i]
    line = line.split()
    for word in line:
        print word + '\t' + '1'
