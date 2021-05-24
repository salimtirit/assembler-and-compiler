from io import open_code


inputfile = open("prog.bin","r")

A = [None]
B = [None]
C = [None]
D = [None]
E = [None]
PC = 0
S = [2**16]


ZF = False
CF = False
SF = False

memory = [None] * 2**16



for line in inputfile:
    line = bin(int(line,16))
    line = str(line)
    line = line[2:]
    while len(line) < 24:
        line = "0"+ line
    memory[PC] = line[0:8]
    PC+=1
    memory[PC] = line[8:16]
    PC+=1
    memory[PC] = line[16:]
    PC+=1

lastInstruction = PC
PC = 0
    


while PC != lastInstruction:
    instruction  = memory[PC]
    opcode = instruction[0:6]
    addrMode = instruction[6:]
    
    PC += 1

    operand1 = memory[PC]
    PC += 1
    operand2 = memory[PC] 
    operand = str(operand1) + str(operand2)

    opcode = int(opcode,2)
    addrMode = int(addrMode,2)

    if opcode == 1:
        break
    elif opcode == 2:
        if addrMode == 0:
            A = operand
        elif addrMode == 1:

        elif addrMode == 2:
        elif addrMode == 3:
        else:
            #what
    elif opcode == 3:
    elif opcode == 4:
    elif opcode == 5:
    elif opcode == 6:
    elif opcode == 7:
    elif opcode == 8:
    elif opcode == 9:
    elif opcode == 10:
    elif opcode == 11:
    elif opcode == 12:
    elif opcode == 13:
    elif opcode == 14:
    elif opcode == 15:
    elif opcode == 16:
    elif opcode == 17:
    elif opcode == 18:
    elif opcode == 19:
    elif opcode == 20:
    elif opcode == 21:
    elif opcode == 22:
    elif opcode == 23:
    elif opcode == 24:
    elif opcode == 25:
    elif opcode == 26:
    elif opcode == 27:
    elif opcode == 28:
    else:
        #what
    PC += 1