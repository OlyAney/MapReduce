from subprocess import Popen, PIPE
import generator
import sys

operation = sys.argv[1]
parameters_ = []
for i in range(2, len(sys.argv)):
    parameters_.append(sys.argv[i])

if operation == "generate":
    n = parameters_[0]
    arg = parameters_[1]
    f_AB = parameters_[2]
    f_BC = parameters_[3]
    generator.generate(n, arg, f_AB, f_BC)

elif operation == "map_reverse":
    path_to_script = parameters_[0]
    f_input_AB = open(parameters_[1], "r")
    f_reversed_AB = open(parameters_[2], "w")
    reverse_map_proc = Popen(["python", path_to_script], stdin=f_input_AB, stdout=PIPE, stderr=PIPE)
    f_reversed_AB.write(reverse_map_proc.communicate()[0])
    f_reversed_AB.close()
    
elif operation == "join_files":
    f_input_BC = open(parameters_[0], "r")
    f_reversed_AB = open(parameters_[1], "r")
    f_BA_BC_joined = open(parameters_[2], "w")
    f_BA_BC_joined.write(f_reversed_AB.read() + f_input_BC.read())
    f_BA_BC_joined.close()

elif operation == "reduce_join":
    path_to_script = parameters_[0]
    f_BA_BC_joined = open(parameters_[1],'r')
    f_joined_by_key = open(parameters_[2], "w")
    data = []
    for line in f_BA_BC_joined:
        data.append(line)
    data.sort()
    reduce_proc = Popen(["python", path_to_script], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    [reduce_proc.stdin.write(i) for i in data]
    f_joined_by_key.write(reduce_proc.communicate()[0])
    reduce_proc.stdin.close()
    f_joined_by_key.close()

elif operation == "split_map":
    path_to_script = parameters_[0]
    f_in = open(parameters_[1], "r")
    f_output = open(parameters_[2], "w")
    split_proc = Popen(["python", path_to_script], stdin=f_in, stdout=PIPE, stderr=PIPE)
    f_output.write(split_proc.communicate()[0])
    f_output.close()
