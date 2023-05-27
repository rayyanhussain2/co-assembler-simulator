import sys

#variables dictionary with opcodes
op_dict = {'00000': ['add', 'A'], '00001': ['sub', 'A'], '00010': ['mov', 'B'], '00011': ['mov_reg', 'C'],
          '00100': ['ld', 'D'], '00101': ['st', 'D'], '00110': ['mul', 'A'], '00111': ['div', 'C'],
          '01000': ['rs', 'B'], '01001': ['ls', 'B'], '01010': ['xor', 'A'], '01011': ['or', 'A'],
          '01100': ['and', 'A'], '01101': ['not', 'C'], '01110': ['cmp', 'C'], '01111': ['jmp', 'E'],
          '11100': ['jlt', 'E'], '11101': ['jgt', 'E'], '11111': ['je', 'E'], '11010': ['hlt', 'F'], 'var': ['', '']}

#register dictionary
register_dict={'000':['R0',"0000000"],'001':['R1',"0000000"],'010':['R2',"0000000"],'011':['R3',"0000000"],'100':['R4',"0000000"],'101':['R5',"0000000"],'110':['R6',"0000000"],'111':['FLAGS', "0000000"]}

#the program counter
pc=0
halt= False
#taking inputs
with open("test.txt","r") as f:
    input_binary_codes = f.readlines()
    input_binary_codes = [i.strip() for i in input_binary_codes]

#Parsing each line of instruction
var_count = 0; label_count = 0; var_dict = {} ; label_dict = {}
i = 0
while True:
    binary_instruction = input_binary_codes[i]
    op_code = binary_instruction[0:5]
    if(op_code=="00000"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1+val2
        if(val>=0 and val<=127):
            register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    elif(op_code=="00001"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1-val2
        
        
        if(val>=0 and val<=127):
            register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    elif(op_code=="00110"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1*val2
        if(val>=0 and val<=127):
            register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    elif(op_code=="01010"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1^val2
        
        if(val>=0 and val<=127):
            register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    elif(op_code=="01011"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1 | val2
        
        if(val>=0 and val<=127):
           register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    elif(op_code=="01100"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1 & val2
        if(val>=0 and val<=127):
           register_dict[binary_instruction[7:10]][1]= "0"*(7-len(bin(val)[2:]))+bin(val)[2:]
    

    elif (op_code == "00100" or op_code == "00101"):
        var_count += 1
        var = "var" + str(var_count)

        mem_address = binary_instruction[-8:-1] 
        if mem_address not in var_dict.values():
            var_dict[var] = mem_address

    elif (op_code in ["01111","11100","11101","11111"]):
        label_count += 1
        label = "label" + str(label_count)

        mem_address = binary_instruction[-8:-1]
        if mem_address not in label_dict.values():   
            label_dict[label] = mem_address

    #Type F
    elif(op_code == "11010"):
        break

    #Type E 
    elif(op_code == "01111"):
        i = int(binary_instruction[5:]) - 1
        continue

    elif(op_code == "11100"):
        if(register_dict[111][1][-3] == '1'):
            i = int(binary_instruction[5:]) - 1
            continue

    elif(op_code == "11101"):
        if(register_dict[111][1][-2] == '1'):
            i = int(binary_instruction[5:]) - 1
            continue
        
    elif(op_code == "11111"):
        if(register_dict[111][1][-1] == '1'):
            i = int(binary_instruction[5:]) - 1
            continue




    #incrementing the counter 
    i += 1