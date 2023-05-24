import sys

#variables dictionary with opcodes
op_dict = {'00000': ['add', 'A'], '00001': ['sub', 'A'], '00010': ['mov', 'B'], '00011': ['mov_reg', 'C'],
          '00100': ['ld', 'D'], '00101': ['st', 'D'], '00110': ['mul', 'A'], '00111': ['div', 'C'],
          '01000': ['rs', 'B'], '01001': ['ls', 'B'], '01010': ['xor', 'A'], '01011': ['or', 'A'],
          '01100': ['and', 'A'], '01101': ['not', 'C'], '01110': ['cmp', 'C'], '01111': ['jmp', 'E'],
          '11100': ['jlt', 'E'], '11101': ['jgt', 'E'], '11111': ['je', 'E'], '11010': ['hlt', 'F'], 'var': ['', '']}

#register dictionary
register_dict={'000':['R0','-'],'001':['R1','-'],'010':['R2','-'],'011':['R3','-'],'100':['R4','-'],'101':['R5','-'],'110':['R6','-'],'111':['FLAGS','-']}

#the program counter
pc=0
halt= False
#taking inputs
with open("test.txt","r") as f:
    input_binary_codes = f.readlines()
    input_binary_codes = [i.strip() for i in input_binary_codes]

var_count = 0; label_count = 0; var_dict = {} ; label_dict = {}
for i in range(len(input_binary_codes)):
    binary_instruction = input_binary_codes[i]
    op_code = binary_instruction[0:5]

    if (op_code == "00100" or op_code == "00101"):
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
