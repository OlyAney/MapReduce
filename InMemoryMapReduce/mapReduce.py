from subprocess import Popen, PIPE
import sys

operation = sys.argv[1]
path_to_script = sys.argv[2]
script_params = []
if len(sys.argv) > 5:
    for i in range(3, len(sys.argv) - 2):
        script_params.append(sys.argv[i])
src_file = sys.argv[len(sys.argv) - 2]
dst_file = sys.argv[len(sys.argv) - 1]
output = open(dst_file, "w")
input = open(src_file, "r")
if operation == "map":
    map_proc = Popen(["python", path_to_script] + script_params, stdin = input, stdout = PIPE, stderr = PIPE)
    input.write(map_proc.communicate()[0])
elif operation == "reduce":
    sort_proc = Popen(["python", str(__file__).strip("mapReduce.py") + "sort.py"], stdin = input, stdout = PIPE, stderr = PIPE)
    reduce_proc = Popen(["python", path_to_script], stdin = sort_proc.stdout, stdout = PIPE, stderr = PIPE)
    output.write(reduce_proc.communicate()[0])
output.close()
