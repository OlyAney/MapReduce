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
f_output = open(dst_file, "w")
f_input = open(src_file, "r")
if operation == "map":
    map_proc = Popen(["python", path_to_script] + script_params, stdin = f_input, stdout = PIPE, stderr = PIPE)
    f_output.write(map_proc.communicate()[0])

elif operation == "reduce":
    sort_proc = Popen(["python", str(__file__).strip("mapReduce.py") + "sort.py"], stdin = f_input, stdout = PIPE, stderr = PIPE)

    key, val = sort_proc.stdout.readline().split('\t')
    in_reduce = key + '\t' + val

    for line in sort_proc.stdout:
        temp_key = line.split('\t')[0]
        if temp_key == key:
            in_reduce += temp_key + '\t' + val
        else:
            key = temp_key
            reduce_proc = Popen(["python", path_to_script], stdin = PIPE, stdout = PIPE, stderr = PIPE)
            f_output.write(reduce_proc.communicate(in_reduce.strip('\n'))[0])
            in_reduce = key + '\t' + val
    reduce_proc = Popen(["python", path_to_script], stdin = PIPE, stdout = PIPE, stderr = PIPE)
    f_output.write(reduce_proc.communicate(in_reduce)[0])

f_output.close()
