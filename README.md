# Python ISA Assembler

This repository contains a Python-based assembler for the **CSE 112 Assignment** instruction set architecture (ISA). 

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
- `sub` Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.
- `mul` - Performs reg1 = reg2 x reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1.
- `xor` - Performs bitwise XOR of reg2 and reg3. Stores the result in reg1.
- `or` - Performs bitwise OR of reg2 and reg3. Stores the result in reg1.
- `and` - Performs bitwise AND of reg2 and reg3. Stores the result in reg1.

Type B
- `mov`
- `rs`
- `ls`

Type C
- `mov`
- `div`
- `not`
- `cmp`

Type D
- `ld`
- `st`
- `cmp`

Type E
- `jmp`
- `jlt`
- `jgt`
- `je`

Type F
- `hlt`

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

## Contributing

Contributions to the assembler are welcome! If you find a bug or have an idea for an improvement, please submit an issue or pull request.

## License

This assembler is released under the [MIT License](https://opensource.org/licenses/MIT).

