import sys

 

variable_dict={}
register_dict={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}



req_file=sys.argv[1]

input_file=open(req_file,'r')
input_assembly_codes=input_file.read().splitlines()
final_assembly_codes=[]
instruction_counter=len(input_assembly_codes)
var_count=0
for i in range (len(input_assembly_codes)):
    if 'var' in input_assembly_codes[i].split():
        var_count+=1
        input_assembly_codes.append(input_assembly_codes[i])





for i in range(len(input_assembly_codes)):
    print(input_assembly_codes[i])

