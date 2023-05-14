import sys

#constant variables
op_dict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['11100', 'E'], 'jgt': ['11101', 'E'], 'je': ['11111', 'E'], 'hlt': ['11010', 'F'], 'var': ['', '']}

register_dict={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}

label_dict = {}

variable_dict={}

final_assembly_codes=[]

machine_code_list=[]

error_indices = []
#------------------------------------------------------------------------------









#input
req_file=sys.argv[1]
input_file=open(req_file,'r')
#these are inputted by user
input_assembly_codes=input_file.read().splitlines()
input_assembly_codes = [i for i in input_assembly_codes if i != ""]

#Parsing for variable allocation
raw_length = len(input_assembly_codes)
instructions_length = len([i for i in input_assembly_codes if i[0:3] != 'var'])
var_memory = instructions_length
var_count = 0
for i in range (len(input_assembly_codes)):
    command = input_assembly_codes[i].split()
    if 'var' in command:
        temp = str(bin(var_memory)[2:])
        temp = "0" * (7 - len(temp)) + temp
        variable_dict[command[1]] = temp
        var_memory += 1
        var_count += 1

#Parsing for label allocation
for i in range(raw_length):
    curr_line = input_assembly_codes[i].split()
    if(curr_line[0][-1] == ':'):
        temp = str(bin(i - var_count)[2:])
        temp = "0"*(7 - len(temp)) + temp
        label_dict[curr_line[0][:-1]] = str(temp)
        temp = input_assembly_codes[i].split()
        temp = " ".join(temp[1:])
        input_assembly_codes[i] = temp

#Conversion of assembly to binary
instruction_size=16
#creating a 2d list to store the indices of the instructions that have errors in them.
#each list within is of the format [index, message, error_type]
hlt_flag=False
used_variables = list()
hlt_counter = 0

#------------------------------------------------------------------------------










#Handling instruction length errors
if(len(input_assembly_codes) > 128):
    error_indices.append([128,'Instruction length exceeds memory size',''])

#parsing the instructions
else:
    #reading through the list of assembly codes and converting to machine and handling errors
    for i in range(len(input_assembly_codes)):
        #Handling the case where the opcodes are valid, else would be the error handling
        #For now, we store the machine code in a list.
        curr_line = input_assembly_codes[i].split()

        #Handling Flags error
        if len(curr_line) == 3:
            if curr_line[2] == "FLAGS" and curr_line[0] != "mov":
                error_indices.append([str(i),"Illegal use of FLAGS register", "d"])
                continue

        elif len(curr_line) == 2:
            if curr_line[1] == "FLAGS":
                error_indices.append([str(i),"Illegal use of FLAGS register", "d"])
                continue

        elif len(curr_line) == 4:
            if "FLAGS" in curr_line:
                error_indices.append([str(i),"Illegal use of FLAGS register", "d"])
                continue

        #Handling case where there are typos in instruction name
        if curr_line[0] in op_dict:
            
            #If opcode is of type A
            if op_dict[curr_line[0]][1]=='A':
                if len(curr_line)==4:
                    #If the registers are valid
                    if(curr_line[1] in register_dict.keys() and curr_line[2] in register_dict.keys() and curr_line[3] in register_dict.keys()):
                        unused_bits=instruction_size-(3*len(register_dict['R0'])+len(op_dict[curr_line[0]][0]))
                        beginning_bits=op_dict[curr_line[0]][0]+unused_bits*'0'
                        register_bits=register_dict[curr_line[1]]+register_dict[curr_line[2]]+register_dict[curr_line[3]]
                        machine_code_list.append(beginning_bits+register_bits)
                    else:
                        #creating a string var to store the error message which contains all the registers that are faulty.
                        #This message will be later parsed and printed out as required.
                        error_message = ""
                        if(curr_line[1] not in register_dict.keys()):
                            error_message += curr_line[1] + " "
                        if(curr_line[2] not in register_dict.keys()):
                            error_message += curr_line[2] + " "
                        if(curr_line[3] not in register_dict.keys()):
                            error_message += curr_line[3] + " "
                        error_indices.append([str(i), error_message, 'a_reg'])
                else:
                    error_indices.append([str(i),"general syntax error"])

            #If opcode is of type B
            elif op_dict[curr_line[0]][1] == 'B' and curr_line[2] not in register_dict.keys():
                imm_flag=True
                if not((isinstance(eval(curr_line[2][1:]), int) == True) and (int(curr_line[2][1:]) >= 0) and (int(curr_line[2][1:]) <= (127))):
                    error_indices.append([str(i), "Illegal immediate value " + curr_line[2][1:], 'e'])
                    imm_flag=False
                
                #If the registers are valid and the immediate value is correct
                if(curr_line[1] in register_dict.keys()):
                    if imm_flag==True:
                        unused_bits = "0" * (1)
                        immidiate_value = str(bin(int(curr_line[2][1:])))
                        immidiate_value = "0" * (7-len(immidiate_value[2:])) + immidiate_value[2:]
                        machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + immidiate_value)
                    else:
                        pass
                else:
                    error_indices.append([str(i), curr_line[1], 'a_reg'])
        
            #If opcode is of type D
            elif op_dict[curr_line[0]][1] == 'D':
                #If the registers are valid and variables are valid
                if(curr_line[1] in register_dict.keys() and curr_line[2] in variable_dict.keys()):
                    unused_bits = "0" * (1)
                    machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + variable_dict[curr_line[2]])
                    #storing all the variables that are used but not declared
                    used_variables.append(curr_line[2])
                else:
                    #if the error lies in register
                    if(curr_line[1] not in register_dict.keys()):
                        error_indices.append([str(i), curr_line[1], 'a_reg'])
                
                    #Label used in place of variable
                    if(curr_line[2] in list(label_dict.keys())):
                        error_indices.append([str(i), f"Label {curr_line[2]} misused here", 'f'])
                    #if the error lies in variable
                    elif(curr_line[2] not in variable_dict.keys()):
                        error_indices.append([str(i), curr_line[2], 'b'])
                        #storing all the variables that are used but not declared
                        used_variables.append(curr_line[2])
        
            #if opcode is of type C
            elif curr_line[0] == 'mov' and curr_line[2] in register_dict.keys():
                #If the registers are valid
                if(curr_line[1] in register_dict.keys() and curr_line[2] in register_dict.keys()):
                    unused_bits = "0" * (5)
                    machine_code_list.append(op_dict['mov_reg'][0] + unused_bits + register_dict[curr_line[1]] + register_dict[curr_line[2]])   
                else:
                    #creating a string var to store the error message which contains all the registers that are faulty.
                    #This message will be later parsed and printed out as required.
                    error_message = ""
                    if(curr_line[1] not in register_dict.keys()):
                        error_message += curr_line[1] + " "
                    if(curr_line[2] not in register_dict.keys()):
                        error_message += curr_line[2] + " "
                    error_indices.append([str(i), error_message, 'a_reg'])

            elif op_dict[curr_line[0]][1] == 'C' :
                #If the registers are valid
                if(curr_line[1] in register_dict.keys() and curr_line[2] in register_dict.keys()):
                    unused_bits = "0" * (5)
                    machine_code_list.append(op_dict[curr_line[0]][0] + unused_bits + register_dict[curr_line[1]] + register_dict[curr_line[2]])
                else:
                    #creating a string var to store the error message which contains all the registers that are faulty.
                    #This message will be later parsed and printed out as required.
                    error_message = ""
                    if(curr_line[1] not in register_dict.keys()):
                        error_message += curr_line[1] + " "
                    if(curr_line[2] not in register_dict.keys()):
                        error_message += curr_line[2] + " "
                    error_indices.append([str(i), error_message, 'a_reg'])
            
            #if op code is of type E
            elif op_dict[curr_line[0]][1] == 'E':

                if(curr_line[1] in label_dict.keys()):
                    unused_bits = "0" * (4)
                    op = op_dict[curr_line[0]][0]
                    mem_ = label_dict[curr_line[1]]           
                    s = op + unused_bits + mem_
                    machine_code_list.append(s)
                else:
                    if (curr_line[1] in list(variable_dict.keys())):
                        error_indices.append([str(i), f"Misuse of variable {curr_line[1]} here", 'f'])
                    else:
                        error_indices.append([str(i), curr_line[1], 'c'])
        
            #if op code is of type F
            elif op_dict[curr_line[0]][1] == 'F':
                s = "1101000000000000"
                machine_code_list.append(s)
        
        else:
            error_indices.append([str(i), "Invalid operation name: " + curr_line[0] , 'a_opcode'])
        
        #Counting number of hlt instances
        if input_assembly_codes[i]=='hlt':
            hlt_flag=True
            hlt_counter += 1

    #Handling hlt errors
    if (hlt_counter <= 1 and input_assembly_codes[-1] != "hlt"):
        error_indices.append([str(i),"Last instruction not hlt",'i'])
    elif hlt_counter > 1:
        error_indices.append([str(i),"Multiple instances of hlt found",'i'])

    #Handling variable declaration error 
    used_variables = list(set(used_variables))
    flag_var = True
    for i in range(len(used_variables)):
        if(input_assembly_codes[i].split()[0] != 'var'):
            flag_var = False
    if not flag_var:
        error_indices.append(["-","Variables not declared in the beginning","g"])    
#------------------------------------------------------------------------------






#printing 
if(len(error_indices) == 0):
          outputfile_name = sys.argv[1][0:-4] + ".bin"
          outputfile = open(outputfile_name,'w')
          outputfile.writelines(line + '\n' for line in machine_code_list[0:len(machine_code_list)-1])
          outputfile.write(machine_code_list[-1])
          outputfile.close()
else:
    print("Error(s) found in the assembly code.")
    print()
    for i in error_indices:
        print("Line: " + str(i[0]) + ": " + i[1])
        print()
#------------------------------------------------------------------------------




#For Debug purpose, shall delete later
'''
print()
print(input_assembly_codes)
print()
print(input_assembly_codes_temp)
print()
print(machine_code_list)
print()
print(variable_dict)
print()
print(register_dict)
print()
print(label_dict)
print()
print(error_indices)
'''
