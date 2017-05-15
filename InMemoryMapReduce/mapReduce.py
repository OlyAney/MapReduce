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
    data = []
    for line in f_input: 
        data.append((line.split(" "))[0]) # вот этого вообще не понял
    data.sort()
    for i in range(len(data)): # или это такой странный код оставшийся с момента когда mapreduce был одной операцией решавшей как раз задачу wordcount
        data[i] += "\t1"
    
    # основная проблема - если сейчас запустить над каким-нибудь файлом последовательно map и reduce оно работать не будет
    # input видимо получен каким-то другим кодом, потому что там в качестве сепараторов используются пробелы а не табы
    # по смыслу как бы всё правильно, но недоработки такие - это не ок
    key, val = data[0].split('\t')
    reduce_proc = Popen(["python", path_to_script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    reduce_proc.stdin.write(key + '\t' + val + '\n')
    for i in range(1, len(data)):
        temp_key = data[i].split('\t')[0]
        if temp_key == key:
           reduce_proc.stdin.write(temp_key + '\t' + val + '\n')
        else:
            f_output.write(reduce_proc.communicate()[0])
            reduce_proc.stdin.close()
            key = temp_key
            reduce_proc = Popen(["python", path_to_script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            reduce_proc.stdin.write(key + '\t' + val + '\n')
    f_output.write(reduce_proc.communicate()[0])
    reduce_proc.stdin.close()

f_output.close()
