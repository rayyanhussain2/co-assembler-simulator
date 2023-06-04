import sys
import Floating_point_precision as fp

#variables dictionary with opcodes
op_dict = {'00000': ['add', 'A'], '00001': ['sub', 'A'], '00010': ['mov', 'B'], '00011': ['mov_reg', 'C'],
          '00100': ['ld', 'D'], '00101': ['st', 'D'], '00110': ['mul', 'A'], '00111': ['div', 'C'],
          '01000': ['rs', 'B'], '01001': ['ls', 'B'], '01010': ['xor', 'A'], '01011': ['or', 'A'],
          '01100': ['and', 'A'], '01101': ['not', 'C'], '01110': ['cmp', 'C'], '01111': ['jmp', 'E'],
          '11100': ['jlt', 'E'], '11101': ['jgt', 'E'], '11111': ['je', 'E'], '11010': ['hlt', 'F'], 'var': ['', '']}

#register dictionary
register_dict={'000':['R0',"0000000000000000"],'001':['R1',"0000000000000000"],'010':['R2',"0000000000000000"],'011':['R3',"0000000000000000"],'100':['R4',"0000000000000000"],'101':['R5',"0000000000000000"],'110':['R6',"0000000000000000"],'111':['FLAGS', "0000000000000000"]}
output = []

#dict
add_dict={};  var_dict = {} ; label_dict = {}

#the program counter
halt= False

#taking inputs
with open("test5.txt","r") as f:
    input_binary_codes = f.readlines()
    #input_binary_codes = sys.stdin.readlines()
    input_binary_codes = [i.strip() for i in input_binary_codes]

#Parsing each line of instruction
var_count = 0; label_count = 0;
i = 0
print(input_binary_codes)

while True:
    pc = i
    flags=False
    binary_instruction = input_binary_codes[i]
    op_code = binary_instruction[0:5]

    #Type A (3 reg)
    #add
    if(op_code=="00000"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1+val2
        if(val>=0 and val<=65535):
            register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]

        elif (val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #sub
    elif(op_code=="00001"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1-val2
        if(val>=0 and val<=127):
            register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]

        elif (val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #Mul
    elif(op_code=="00110"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1*val2
        if(val>=0 and val<=65535):
            register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]
        elif (val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True


    #xor
    elif(op_code=="01010"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1^val2
        if(val>=0 and val<=65535):
            register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]
        elif(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True


    #or
    elif(op_code=="01011"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1 | val2
        if(val>=0 and val<=65535):
           register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]
        elif(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True


    #and
    elif(op_code=="01100"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)
        val=val1 & val2
        if(val>=0 and val<=65535):
           register_dict[binary_instruction[7:10]][1]= "0"*(16-len(bin(val)[2:]))+bin(val)[2:]
        elif(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #Type B (reg - $IMM)
    #mov
    elif(op_code=="00010"):
        val=int(("0b"+binary_instruction[9:]),2)
        if(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True
        else:
            register_dict[binary_instruction[6:9]][1]="0"*(16-len(bin(val)[2:]))+bin(val)[2:]


    #rs
    elif(op_code=="01000"):
        val="0b"+binary_instruction[9:]
        val=int(val,2)
        nval=register_dict[binary_instruction[6:9]][1]
        nval=int("0b"+nval,2)
        nval= nval >> val
        if(nval>=0 and nval<=65535):
            register_dict[binary_instruction[6:9]][1]="0"*(16-len(bin(nval)[2:]))+bin(nval)[2:]
        elif(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #ls
    elif(op_code=="01001"):
        val="0b"+binary_instruction[9:]
        val=int(val,2)
        nval=register_dict[binary_instruction[6:9]][1]
        nval=int("0b"+nval,2)
        nval= nval << val
        if(nval>=0 and nval<=65535):
            register_dict[binary_instruction[6:9]][1]="0"*(16-len(bin(nval)[2:]))+bin(nval)[2:]
        elif(val > 65535):
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

  

    #Type F
    elif(op_code == "11010"):
        halt = True

    #Type E 
    elif(op_code == "01111"):
        i = int("0b"+binary_instruction[5:],2) - 1
        

    elif(op_code == "11100"):
        if(register_dict["111"][1][-3] == '1'):
            i = int("0b"+binary_instruction[5:],2) - 1
            

    elif(op_code == "11101"):
        if(register_dict["111"][1][-2] == '1'):
            i = int("0b"+binary_instruction[5:],2) - 1
            
        
    elif(op_code == "11111"):
        if(register_dict["111"][1][-1] == '1'):
            i = int("0b"+binary_instruction[5:],2) - 1
            

    #type C
    #mov R1 R2
    elif(op_code == "00011"):
        register_dict[binary_instruction[10:13]][1] = register_dict[binary_instruction[13:16]][1]

    #Invert
    elif(op_code == "01101"):
        regval2 = "0b" + register_dict[binary_instruction[13:16]][1]
        regval2 = ~int(regval2, 2)
        regval2 = bin(regval2)
        regval2 = "0"* (16 - len(regval2[2:])) + regval2[2:]
        register_dict[binary_instruction[10:13]][1] = regval2

    #compare
    elif(op_code == "01110"):
        val1="0b"+register_dict[binary_instruction[10:13]][1]
        val2="0b"+register_dict[binary_instruction[13:16]][1]
        val1=int(val1,2)
        val2=int(val2,2)

        if val1>val2:
            register_dict["111"][1] = 12*"0" + "0010"
            flags=True
        elif val1<val2:
            register_dict["111"][1] = 12*"0" + "0100"
            flags=True
        elif val1==val2:
            register_dict["111"][1] = 12*"0" + "0001"
            flags=True

    #div
    elif(op_code=="00111"):
        val1="0b" + register_dict[binary_instruction[10:13]][1]
        val2="0b" + register_dict[binary_instruction[13:16]][1]
        val1,val2=int(val1,2),int(val2,2)

        #Denominator is zero. Infinite
        if val2 == 0:
            register_dict["111"][1][-4]="1"
            register_dict['000'][1]="0"*(16)
            register_dict['001'][1]="0"*(16)
            
        else:
            valQ=val1//val2
            valR=val1%val2

            if (valQ > 65535):
                register_dict["111"][1] = 12*"0" + "1000"
                flags=True
            else:
                register_dict['000'][1]="0"*(16-len(bin(valQ)[2:]))+bin(valQ)[2:]
                register_dict['001'][1]="0"*(16-len(bin(valR)[2:]))+bin(valR)[2:]


    #Type D(reg - mem)
    #store
    elif(op_code=="00101"):
        var_dict[binary_instruction[9:]] = register_dict[binary_instruction[6:9]][1]

    #load
    elif(op_code=="00100"):
        if(binary_instruction[9:] not in var_dict.keys()):
            var_dict[binary_instruction[9:]] = "0" * (16)
        register_dict[binary_instruction[6:9]][1]= var_dict[binary_instruction[9:]]      



    #add float
    elif(op_code=="10000"):
        val1=fp.floating_point_precision_val(register_dict[binary_instruction[10:13]][1])
        val2=fp.floating_point_precision_val(register_dict[binary_instruction[13:16]][1])
        val = val1+val2
        val_b = fp.floating_point_precision_bin(val)
        if 0<=val_b<=31.5:
            register_dict[binary_instruction[7:10]][1]= "0"*(16 - len(val_b))+ val_b
        elif val_b > 31.5:
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #sub float
    elif(op_code=="10001"):
        val1=fp.floating_point_precision_val(register_dict[binary_instruction[10:13]][1])
        val2=fp.floating_point_precision_val(register_dict[binary_instruction[13:16]][1])
        val = val1-val2
        val_b = fp.floating_point_precision_bin(val)
        if 0<=val_b<=31.5:
            register_dict[binary_instruction[7:10]][1]= "0"*(16 - len(val_b))+ val_b
        elif val_b > 31.5:
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #move float
    elif(op_code=="10010"):
        val=binary_instruction[9:]
        if 0<=val<=31.5:
            register_dict[binary_instruction[6:9]][1]="0"*(16-len(val))+val
        elif val > 31.5:
            register_dict["111"][1] = 12*"0" + "1000"
            flags=True

    #Getting the status
    pc_b = str(bin(pc))[2:]
    
    pc_b = "0"*(7 - len(pc_b)) + pc_b


    if flags==True:
        pass
    else:
        register_dict["111"][1]=16*"0"

    line = pc_b
    line += "        "
    for k in list(register_dict.values()):
        
        line += str(k[1])
        line += " "

    print(line[:len(line)-1])
    if halt == True:
        break

    #Incrementing pc
    i+=1


#Dumping memory
k = 0 #Indicating line_no
for i in input_binary_codes:
    b = str(bin(k)[2:])
    b = "0"*(7 - len(b)) + b
    l = f"{i}"
    print(l)
    k+=1

for i in list(var_dict.keys()):
    b = str(bin(k)[2:])
    b = "0"*(7 - len(b)) + b
    l = f"{var_dict[i]}"
    print(l)
    k+=1

line = (128 - len(input_binary_codes) - len(var_dict))*"0000000000000000\n"
print(line)