from subprocess import Popen, PIPE
from merge import Merger
import os
import sys

# creating a temporary file that can fit into main memory records (sorted by key)
def sort_and_write(chunks, index): # так chunk или chunks ? всё-таки кажется первое
    chunks.sort()
    temp_f = "tmp_{0}.txt".format(index)
    with open(temp_f, "w") as f:
        for item in chunks:
            f.write(item)
    del chunks[:] # вероятно [:] тут лишнее ?
    return temp_f

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
    map_proc = Popen(["python", path_to_script] + script_params, stdin=f_input, stdout=PIPE, stderr=PIPE)
    f_output.write(map_proc.communicate()[0])

elif operation == "reduce": # хорошая практика ругаться если ваша программа не запускается из-за неверного списка параметров
    # сейчас она молча завершается и неясно - всё хорошо или нет
    max_size = 20000
    temp_paths = []
    i = 0
    while True:
        chunk = f_input.readlines(max_size)
        if not chunk:
            break
        else:  
            temp_file = sort_and_write(chunk, i)
            temp_paths.append(temp_file)
        i += 1
    # i= 0
    # while True:
    #     chunk = f_input.read(max_size)
    #     if chunk == "":
    #         break
    #     else:
    #         if not chunk.endswith("\n"):
    #             while not chunk.endswith("\n"):
    #                 f_input.seek(f_input.tell() - 1, 0)
    #                 chunk = chunk[:-1]
    #         temp_file = sort_and_write(chunk, i)
    #         temp_paths.append(temp_file)
    #     i += 1
    #
    merger_output_name = "merger_output.txt"
    merger = Merger(merger_output_name)
    merger.merge(temp_paths)

    in_reduce = open(merger_output_name, "r")

    key, val = in_reduce.readline().strip('\n').split()
    reduce_proc = Popen(["python", path_to_script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    reduce_proc.stdin.write(key + '\t' + val + '\n')
    try:
        while True:
            temp_key, temp_val = in_reduce.readline().strip('\n').split()
            if temp_key == key:
                reduce_proc.stdin.write(temp_key + '\t' + temp_val + '\n')
            else:
                f_output.write(reduce_proc.communicate()[0])
                reduce_proc.stdin.close()
                key = temp_key
                reduce_proc = Popen(["python", path_to_script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                reduce_proc.stdin.write(key + '\t' + temp_val + '\n')
    except:
        f_output.write(reduce_proc.communicate()[0])
        reduce_proc.stdin.close()

os.remove(merger_output_name)
f_output.close()
