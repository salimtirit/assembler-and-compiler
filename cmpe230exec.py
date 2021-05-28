from io import open_code

inputfile = open("prog.bin","r")

#Registers
A = [None]
B = [None]
C = [None]
D = [None]
E = [None]
S = 2**16  # [2**16]  Which one?
PC = 0
CF = 0
ZF = False
SF = False

memory = [None] * 2**16

registers = {
    "0000" : PC,
    "0001" : A,
    "0002" : B,
    "0003" : C,
    "0004" : D,
    "0005" : E,
    "0006" : S
}

def adjust_flag(data) :
    if data == bin_zero :    #adjust ZF
        ZF = True
    else :
        ZF = False

    if data[0] == "1" :  #adjust SF
        SF = True      #also take 2's complement maybe, then return
    else :
        SF = False
    return data

def not_numb(data) :
    for i in range(len(data)) :
        if data[i] == 1 :
            data[i] = 0
        else :
            data[i] = 1

def addition (data, addend):
    i = len(data)
    sum = ""
    while i != 0 :
        temp = CF + data[i] + addend[i]
        if temp > 1 : 
            CF = 1
            sum = str(temp-2) + sum
        else :
            CF = 0
            sum = str(temp) + sum 
        i -= 1   
    
    sum = adjust_flag(sum)
    return sum

for line in inputfile:
    line = bin(int(line,16))   # hex -> binary
    line = str(line)
    line = line[2:]  # deleting '0b' part 
    while len(line) < 24:  # adding missing '0's
        line = "0"+ line
    memory[PC] = line[0:8]  # loading them to memory
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
    opcode = int(opcode,2)
    operand_hex = hex(int(operand,2))
    operand_hex = operand[2:]

    addrMode = instruction[6:]
    addrMode = int(addrMode,2)

    PC += 1
    operand1 = memory[PC]
    PC += 1
    operand2 = memory[PC] 
    operand = str(operand1) + str(operand2)

    bin_one = "0000000000000001"
    bin_zero = "0000000000000000"

    #taking the data
    if addrMode == 0 :
        data  = operand
    elif addrMode == 1 :
        data = registers[operand_hex][0]
    elif addrMode == 2 :
        memo_address = registers[operand_hex][0]
        memo_address = int(memo_address,2)
        data = memory[memo_address] + memory[memo_address+1] 
    else :
        memo_address = int(operand,2)
        data = memory[memo_address] + memory[memo_address+1] 


    if opcode == 1:  #HALT
        break
    elif opcode == 2:    #LOAD
        A[0] = data
    elif opcode == 3:   #STORE
        if addrMode == 1 : #register is given
            registers[operand_hex][0] = A[0]
        elif addrMode == 2 :
            memory[memo_address] = A[0][:8]
            memory[memo_address + 1] = A[0][8:]

    elif opcode == 4:   #ADD
        sum = addition(data, A[0])
        sum = bin(sum)
        A[0] = sum[2:]

    elif opcode == 5:   #SUB
        operand = not_numb(data)
        operand = addition(operand, bin_one)
        sub = addition(A[0], operand)
        sub = bin(sub)
        A[0] = sub[2:]
        
    elif opcode == 6:   #INC
        inc = addition(data, bin_one)
        if addrMode == 1 :
            registers[operand_hex][0] = inc
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = inc[:8]
            memory[memo_address + 1] = inc[8:]
        
    elif opcode == 7:   #DEC
        not_bin_one = not_numb(bin_one)
        dec = addition(data, not_bin_one)
        if addrMode == 1 :
            registers[operand_hex][0] = inc
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = dec[:8]
            memory[memo_address + 1] = dec[8:]
        
    elif opcode == 8:   #XOR
        xor = ""
        for i in range(len(data)) :
            if A[0][i] == data[i] :
                xor = xor + "0"
            else :
                xor = xor + "1"

        xor = adjust_flag(xor)
        A[0] = xor

    elif opcode == 9:   #AND
        operand_and = ""
        for i in range(len(data)) :
            if (A[0][i] == "1") and (data[i] == "1") :
                operand_and = operand_and + "1"
            else :
                operand_and = operand_and + "0"

        operand_and = adjust_flag(operand_and)
        A[0] = operand_and

    elif opcode == 10:  #OR
        operand_or = ""
        for i in range(len(data)) :
            if (A[0][i] == "0") and (data[i] == "0") :
                operand_or = operand_or + "0"
            else :
                operand_or = operand_or + "1"

        operand_or = adjust_flag(operand_or)
        A[0] = operand_or

    elif opcode == 11:  #NOT
        operand_not = not_numb(data)
        if addrMode == 1 :
            registers[operand_hex][0] = operand_not
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = operand_not[:8]
            memory[memo_address + 1] = operand_not[8:]
             
    elif opcode == 12:  #SHL
        data = data[1:] + "0"
        registers[operand_hex][0] = data

    elif opcode == 13:  #SHR
        data = + "0" + data[:-1]
        registers[operand_hex][0] = data

    elif opcode == 14:  #NOP
        continue

    elif opcode == 15:  #PUSH
        memory[S] = data[:8]
        S -= 1
        memory[S] = data[8:]
        S -= 1

    elif opcode == 16:  #POP
        registers[operand_hex][0] = memory[S+1] + memory[S]
        S += 2 

    elif opcode == 17:  #CMP
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
