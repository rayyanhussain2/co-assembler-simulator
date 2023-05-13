import sys

op_dict = {'add': ['00000', 'A'], 'sub': ['00001', 'A'], 'mov': ['00010', 'B'], 'mov_reg': ['00011', 'C'],
          'ld': ['00100', 'D'], 'st': ['00101', 'D'], 'mul': ['00110', 'A'], 'div': ['00111', 'C'],
          'rs': ['01000', 'B'], 'ls': ['01001', 'B'], 'xor': ['01010', 'A'], 'or': ['01011', 'A'],
          'and': ['01100', 'A'], 'not': ['01101', 'C'], 'cmp': ['01110', 'C'], 'jmp': ['01111', 'E'],
          'jlt': ['11100', 'E'], 'jgt': ['11101', 'E'], 'je': ['11111', 'E'], 'hlt': ['11010', 'F'], 'var': ['', '']}

inst_list = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp',
             'jmp', 'jlt', 'jgt', 'je', 'hlt']

register_dict={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}



#req_file=sys.argv[1]
req_file='input51.txt'


input_file=open(req_file,'r')
#these are inputted by user
input_assembly_codes=input_file.read().splitlines()


#Parsing for variable allocation
final_assembly_codes=[]
instruction_counter=len(input_assembly_codes)
var_count=0
var_memory = instruction_counter + 1
variable_dict={}
for i in range (len(input_assembly_codes)):
    command = input_assembly_codes[i].split()
    if 'var' in command:
        var_count += 1
        temp = str(bin(var_memory)[2:])
        temp = "0"*(7 - len(temp)) + temp
        variable_dict[command[1]] = temp
        var_memory += 1
        #input_assembly_codes.append(input_assembly_codes[i])


label_dict = {}
#Parsing for label allocation
for i in range(instruction_counter):
          #these are line-wise commands
    curr_line = input_assembly_codes[i].split()
    if(curr_line[0][-1] == ':'):
        temp = str(bin(i+1)[2:])
        temp = "0"*(7 - len(temp)) + temp
        label_dict[curr_line[0][:-1]] = str(temp)
        temp = input_assembly_codes[i].split()
        temp = " ".join(temp[1:])
        input_assembly_codes[i] = temp

#Conversion of assembly to binary
instruction_size=16
machine_code_list=[]
#creating a 2d list to store the indices of the instructions that have errors in them.
#each list within is of the format [index, message, error_type]
error_indices = []
hlt_flag=False
used_variables = list()

#reading through the list of assembly codes and converting to machine
for i in range(len(input_assembly_codes)):
    #Handling the case where the opcodes are valid, else would be the error handling
    #For now, we store the machine code in a list.
    curr_line = input_assembly_codes[i].split()
    if len(curr_line) == 3:
        if curr_line[2] == "FLAGS" and curr_line[0] != "mov":
            error_indices.append([str(i),"ILLEGAL USE OF FLAGS REGISTER", "d"])
            continue

    elif len(curr_line) == 2:
        if curr_line[1] == "FLAGS":
            error_indices.append([str(i),"ILLEGAL USE OF FLAGS REGISTER", "d"])
            continue

    elif len(curr_line) == 4:
        if "FLAGS" in curr_line:
            error_indices.append([str(i),"ILLEGAL USE OF FLAGS REGISTER", "d"])
            continue

    
    if curr_line[0] in op_dict:
        #If opcode is of type A
        if op_dict[curr_line[0]][1]=='A':
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

        #If opcode is of type B
        elif op_dict[curr_line[0]][1] == 'B' and curr_line[2] not in register_dict.keys():
            imm_flag=True
            if(int(curr_line[2][1:])<0 or int(curr_line[2][1:])>= (2**7)):
                error_message="illegal immediate value"
                error_indices.append([str(i),error_message,'e'])
                imm_flag=False
            #If the registers are valid
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
            s = "1001100000000000"
            machine_code_list.append(s)
    #Handling case where there are typos in instruction name
    else:
        error_indices.append([str(i), "Invalid operation name: " + curr_line[0] , 'a_opcode'])
    
    
    if input_assembly_codes[i]=='hlt':
        hlt_flag=True
    if i==len(input_assembly_codes)-1:
        if input_assembly_codes[i]!='hlt':
            error_indices.append([str(i),"Last instruction not hlt",'i'])
if hlt_flag==False:
    error_indices.append(["no hlt present",'h'])


used_variables = list(set(used_variables))
flag_var = True
for i in range(len(used_variables)):
    if(input_assembly_codes[i].split()[0] != 'var'):
        flag_var = False

if not flag_var:
    error_indices.append(["-","Variables not declared in the beginning","g"])    
    

if(len(error_indices) == 0):
      
          outputfile = open('output.txt','w')
          outputfile.writelines(line + '\n' for line in machine_code_list)
          outputfile.close()
else:
        fh2=open('error_bin.txt','w')
        err_list=[]
        for i in range(len(error_indices)):
            output_str=""
            for j in range(len(error_indices[i])):
                output_str+=(error_indices[i][j]+" ")
            err_list.append(output_str)
        fh2.writelines(line + '\n' for line in err_list)
            
  
          
    



#For Debug purpose, shall delete later
print(input_assembly_codes)
print(machine_code_list)
print()
print(variable_dict.keys())
print()
print(register_dict.keys())
print()
print(error_indices)
