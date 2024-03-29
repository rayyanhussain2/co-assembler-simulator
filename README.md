# Python ISA Assembler

This repository contains a Python-based assembler for the instruction set architecture (ISA) that is created specifically for the Computer Organization course (CSE 112) offered at Indraprastha Institute of Information Technology Delhi for the Academic Year 2022 - 23. 

## Requirements

To use this assembler, you must have Python 3.x installed on your computer. 

## Usage

To use the assembler, simply run the `assembler.py` script with the file name of the assembly code you wish to assemble as the argument:

```
python assembler.py <assembly_file>
```

The assembler will then generate a binary file containing the assembled machine code, with the same name as the assembly file but with a `.bin` extension.

## Supported Instructions

The ISA has 6 encoding types of instructions. The assembler supports the following instructions:

Type A
- `add`
    
    Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1
- `sub`

    Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.
- `mul`

    Performs reg1 = reg2 x reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1.
- `xor`
    
    Performs bitwise XOR of reg2 and reg3. Stores the result in reg1.
- `or`

    Performs bitwise OR of reg2 and reg3. Stores the result in reg1.
- `and`
    
    Performs bitwise AND of reg2 and reg3. Stores the result in reg1.

Type B
- `mov`

    Performs reg1 = $Imm where Imm is a 7 bit value.
- `rs`

    Right shifts reg1 by $Imm, where $Imm is a 7 bit value.
- `ls`

    Left shifts reg1 by $Imm, where $Imm is a 7 bit value.

Type C
- `mov`

    Move content of reg2 into reg1.
- `div`

    Performs reg3/reg4. Stores the quotient in R0 and the remainder in R1. If reg4 is 0 then overflow flag is set and content of R0 and R1 are set to 0
- `not`

    Performs bitwise NOT of reg2. Stores the result in reg1.
- `cmp`

    Compares reg1 and reg2 and sets up the FLAGS register.

Type D
- `ld`

    Loads data from mem_addr into reg1.
- `st`

    Stores data from reg1 to mem_addr.

Type E
- `jmp`

    Jumps to mem_addr, where mem_addr is a memory address.
- `jlt`

    Jump to mem_addr if the less than flag is set (less than flag = 1), where mem_addr is a memory address.
- `jgt`

    Jump to mem_addr if the greater than flag is set (greater than flag= 1), where mem_addr is a memory address.
- `je`
    
    Jump to mem_addr if the equal flag is set (equal flag = 1), where mem_addr is a memory address.

Type F
- `hlt`
    
    Stops the machine from executing until reset

## Assembly Syntax

The assembler uses a simplified syntax for the assembly code. The following are examples of the syntax for the various types of instructions:


Type A
```
<instruction> <reg 1> <reg 2> <reg 3>
```

Type B
```
<instruction> <reg 1> <$Imm>
```

Type C
```
<instruction> <reg 1> <reg 2>
```

Type D
```
<instruction> <reg 1> <mem_addr>
```

Type E
```
<instruction> <mem_addr>
```

Type F
```
<instruction>
```

## Example

An example assembly code file named `example.asm` is included in the repository. To assemble it, run the following command:

```
python assembler.py example.asm
```

This will generate a binary file named `example.bin` containing the assembled machine code.


# Python ISA Assembler

This repository contains a Python-based simulator for the instruction set architecture (ISA) that is created specifically for the Computer Organization course (CSE 112) offered at Indraprastha Institute of Information Technology Delhi for the Academic Year 2022 - 23. 

## Requirements

To use this simulator, you must have Python 3.x installed on your computer. 

## Usage

To use the simulator, simply run the `simulator.py` script with the file name of the binary output code you wish to simulate as the argument:

```
python simulator.py <outputbinary_file>
```
##Components

# Python ISA Assembler

- `Memory (MEM)`
   MEM takes in a 7-bit address and returns a 16-bit value as the data
   The MEM stores 256 bytes, initialized to 0s
   
- `Program Counter (PC)`
   The PC is a 7-bir register that points to the current instruction

- `Register File (RF)`
   The RF takes is the register name (R0, R1, R2 ... R6 or FLAGS) and returns the
   value stores at that register

- `Execution Engine (EE)`
   The EE takes the address of the instruction from MEM, and executes the instruction
   by updating the RF and PC

## Pseudocode
```
initialize(MEM);
PC=0;
halted = false;

while(not halted)
{
    Instruction = MEM.fetchData(PC);
    halted, new_PC = EE.execute(Instruction);
    PC.dump();
    RF.dump();
    PC.update(new_PC);
}

MEM.dump();
```

## Floating-Point Arithmetic
- `F_addition`
    
    Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set and
    reg 1 is set to 0
- `F_subtraction`

    Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.
- `Move F_immediate`

    Performs reg1 = $Imm where Imm is an 8-bit floating point value








## Contributing

Contributions to the assembler are welcome! If you find a bug or have an idea for an improvement, please submit an issue or pull request.

## License

This assembler is released under the [MIT License](https://opensource.org/licenses/MIT).

