# Assembler and Execution Simulator

This project consists of an assembler and an execution simulator for a hypothetical CPU called CPU230. The assembler translates assembly code written in a high-level language into machine code that can be executed by the CPU230. The execution simulator, on the other hand, takes the machine code and simulates the execution of the program step by step.

## CPU230 Architecture

CPU230 is a simple CPU that has the following architecture:

![CPU230 Architecture](https://user-images.githubusercontent.com/64011660/233503805-ce59f428-9f36-45a1-a15a-012f1017f171.png)

Each instruction has a fixed length of 3 bytes with the following format:

| Opcode (6 bits) | Addressing mode (2 bits) | Operand (16 bits) |
| --- | --- | --- |
| 6 bits | 2 bits | 16 bits |

The addressing modes are as follows:

| Addressing mode bits | Addressing mode |
| --- | --- |
| 00 | Operand is immediate data |
| 01 | Operand is given in the register |
| 10 | Operand’s memory address is given in the register |
| 11 | Operand is a memory address |

Registers are represented as bit patterns, given in hex:

```
PC=0000, A=0001, B=0002, C=0003, D=0004, E=0005, S=0006.
```

## Instructions

The following instructions are supported by CPU230:

| Instruction | Instruction code (hex) | Operand | Meaning | Flags set |
| --- | --- | --- | --- | --- |
| HALT | 1 | - | Halts the CPU. | - |
| LOAD | 2 | immediate / memory / register | Loads operand onto A. | - |
| STORE | 3 | memory / register | Stores value in A to the operand. | - |
| ADD | 4 | immediate / memory / register | Adds operand to A. Perform the addition by treating all the bits as unsigned integer. | CF, SF, ZF |
| SUB | 5 | immediate / memory / register | Subtracts operand (OPR) from A. Implemented as ADD instruction as follows: A - OPR = A + not(OPR) + 1 | CF, SF, ZF |
| INC | 6 | immediate / memory / register | Increments operand (equivalent to add 1) | SF, ZF, CF |
| DEC | 7 | immediate / memory / register | Decrements operand (equivalent to sub 1) | SF, ZF, CF |
| XOR | 8 | immediate / memory / register | Bitwise XOR operand with A and store result in A. | SF, ZF |
| AND | 9 | immediate / memory / register | Bitwise AND operand with A and store result in A. | SF, ZF |
| OR | A | immediate / memory / register | Bitwise OR operand with A and store result in A. | SF, ZF |
| NOT | B | immediate / memory / register | Take complement of the bits of the operand. | SF, ZF |
| SHL | C | register | Shift the bits of register one position to the left. | SF, ZF, CF |
| SHR | D | register | Shift the bits of register one position to the right. | SF, ZF |
| NOP | E | - | No operation. | - |
| PUSH | F | register | Push a word sized operand (two bytes) and update S by subtracting 2. | - |
| POP | 10 | register | Pop a word sized data (two bytes) into the operand and update S by adding 2. | - |
| CMP | 11 | immediate / memory / register | Perform comparison between A-operand and specified operand and set flags accordingly | SF, ZF, CF |
| JMP | 12 | immediate | Unconditional jump to specified address | None |
| JZ/JE | 13 | immediate | Jump to specified address if zero flag is true | None |
| JNZ/JNE | 14 | immediate | Jump to specified address if zero flag is false | None |
| JC | 15 | immediate | Jump to specified address if carry flag is true | None |
| JNC | 16 | immediate | Jump to specified address if carry flag is false | None |
| JA | 17 | immediate | Jump to specified address if above (unsigned comparison) | None |
| JAE | 18 | immediate | Jump to specified address if above or equal (unsigned comparison) | None |
| JB | 19 | immediate | Jump to specified address if below (unsigned comparison) | None |
| JBE | 1A | immediate | Jump to specified address if below or equal (unsigned comparison) | None |
| READ | 1B | memory / register | Reads a character into the specified operand | None |
| PRINT | 1C | immediate / memory / register | Prints the specified operand as a character | None |
