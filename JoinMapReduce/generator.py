from random import randint

def generate(n, arg, f_name_AB, f_name_BC):
    arg = int(arg)
    file_AB = open(f_name_AB, "w")
    file_BC = open(f_name_BC, "w")
    for i in range(int(n)):
        file_AB.write(str(randint(0, arg)) + '\t' + str(randint(0, arg)) + '\n')
        file_BC.write(str(randint(0, arg)) + '\t' + str(randint(0, arg)) + '\n')
    file_AB.close()
    file_BC.close()