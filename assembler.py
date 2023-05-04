import sys

op_dict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['10000', 'E'], 'jgt': ['10001', 'E'], 'je': ['10010', 'E'], 'hlt': ['10011', 'F']}

inst_list = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp',
             'jmp', 'jlt', 'jgt', 'je', 'hlt']

variable_dict={}
register_dict={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}



#req_file=sys.argv[1]
req_file='input1.txt'


input_file=open(req_file,'r')
input_assembly_codes=input_file.read().splitlines()

#Parsing for variable allocation
final_assembly_codes=[]
instruction_counter=len(input_assembly_codes)
var_count=0
var_memory = instruction_counter + 1
var_dict = {}
for i in range (len(input_assembly_codes)):
    command = input_assembly_codes[i].split()
    if 'var' in command:
        var_count+=1
        temp = str(bin(var_memory)[2:])
        temp = "0"*(7 - len(temp)) + temp
        var_dict[command[1]] = temp
        var_memory += 1
        #input_assembly_codes.append(input_assembly_codes[i])


label_dict = {}
#Parsing for label allocation
for i in range(instruction_counter):
    curr_line = input_assembly_codes[i].split()
    if(curr_line[0][-1] == ':'):
        temp = str(bin(i)[2:])
        temp = "0"*(7 - len(temp)) + temp
        label_dict[curr_line[0][:-1]] = str(temp)
        temp = input_assembly_codes[i].split()
        temp = " ".join(temp[1:])
        input_assembly_codes[i] = temp

#reading through the list of assembly codes and converting to machine
instruction_size=16
machine_code_list=[]
for i in range(len(input_assembly_codes)):
    #Handling the case where the opcodes are valid, else would be the error handling
    #For now, we store the machine code in a list.
    curr_line = input_assembly_codes[i].split() 
    if curr_line[0] in op_dict:
        #If opcode is of type A
        if op_dict[curr_line[0]][1]=='A':
            unused_bits=instruction_size-(3*len(register_dict['R0'])+len(op_dict[curr_line[0]][0]))
            beginning_bits=op_dict[curr_line[0]][0]+unused_bits*'0'
            register_bits=register_dict[curr_line[1]]+register_dict[curr_line[2]]+register_dict[curr_line[3]]
            machine_code_list.append(beginning_bits+register_bits)
        #If opcode is of type B
        elif op_dict[curr_line[0]][1] == 'B' and curr_line[2] not in register_dict.keys():
            unused_bits = "0" * (1)
            immidiate_value = str(bin(int(curr_line[2][1:])))
            immidiate_value = "0" * (7-len(immidiate_value[2:])) + immidiate_value[2:]
            machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + immidiate_value)
        #If opcode is of type D
        elif op_dict[curr_line[0]][1] == 'D':
            unused_bits = "0" * (1)
            machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + var_dict[curr_line[2]])
        #if opcode is of type C
        elif op_dict[curr_line[0]][1] == 'C':
            unused_bits = "0" * (5)
            machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + var_dict[curr_line[2]])

        #if op code is of type E
        elif op_dict[curr_line[0]][1] == 'E':
            unused_bits = "0" * (4)
            op = op_dict[curr_line[0]][0]

            if curr_line[1] in var_dict:
                mem_ = var_dict[curr_line[1]]
            elif curr_line[1] in label_dict:
                mem_ = label_dict[curr_line[1]]
            
            s = op + unused_bits + mem_
            machine_code_list.append(s)
        #if op code is of type F
        elif op_dict[curr_line[0]][1] == 'F':
            break

          

#For Debug purpose, shall delete later
print(machine_code_list)
