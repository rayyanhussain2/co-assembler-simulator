import sys

 

variable_dict={}
register_dict={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}



#req_file=sys.argv[1]
req_file='input1.txt'


input_file=open(req_file,'r')
input_assembly_codes=input_file.read().splitlines()
final_assembly_codes=[]
instruction_counter=len(input_assembly_codes)
var_count=0
for i in range (len(input_assembly_codes)):
    if 'var' in input_assembly_codes[i].split():
        var_count+=1
        input_assembly_codes.append(input_assembly_codes[i])


label_dict = {}
#Reading for label allocation
for i in range(instruction_counter):
    if(input_assembly_codes[i].split()[0][-1] == ':'):
        temp = str(bin(i)[2:])
        temp = "0"*(7 - len(temp)) + temp
        label_dict[input_assembly_codes[i].split()[0][:-1]] = str(temp)
        temp = input_assembly_codes[i].split()
        temp = " ".join(temp[1:])
        input_assembly_codes[i] = temp
