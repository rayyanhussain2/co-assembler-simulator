



variable_dict={}
register_dict={'R0':'0000000000000000','R1':'0000000000000001','R2':'0000000000000010','R3':'0000000000000011','R4':'0000000000000100','R5':'0000000000000101','R6':'0000000000000110','FLAGS':'0000000000000111'}





input_file=open('input1.txt','r')
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

