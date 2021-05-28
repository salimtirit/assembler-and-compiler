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
CF = 0
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
        temp_sum = CF + data[i] + addend[i]
        if temp_sum > 1 : 
            CF = 1
            sum = str(temp_sum-2) + sum
        else :
            CF = 0
            sum = str(temp_sum) + sum 

        if sum == 0:
           ZF = True
        else :
            ZF = False
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
    addrMode = instruction[6:]
    PC += 1
    operand1 = memory[PC]
    PC += 1
    operand2 = memory[PC] 
    operand = str(operand1) + str(operand2)

    operand_hex = hex(int(operand,2))
    operand_hex = operand[2:]

    opcode = int(opcode,2)
    addrMode = int(addrMode,2)
    bin_one = "0000000000000001"

    #taking the data
    if addrMode == 0 :
        data  = operand
    elif addrMode == 1 :
        data = registers[operand_hex]
    elif addrMode == 2 :
        memo_address = registers[operand_hex]
        data = int(memory[memo_address],2)
        data = data[2:]
    else :
        memo_address = int(operand,2)
        memo_address = memo_address[2:]
        data = memory[memo_address]


    if opcode == 1:  #HALT
        break
    elif opcode == 2:    #LOAD
        A = data
    elif opcode == 3:       #STORE
        if addrMode == 1 : #register is given
            registers[operand_hex] = A[0]
        elif addrMode == 2 :
            memo_address = registers[operand_hex] #get memory address from register
            memo_address = int(memo_address,2) #Not sure if it's binary
            memo_address = memo_address[2:]
            memory[memo_address] = A[0]

    elif opcode == 4:   #ADD
        addend = A[0]
        sum = addition(data, addend)
        sum = bin(sum)
        A[0] = sum[2:]

    elif opcode == 5:   #SUB
        minuend = A[0]
        opr = not_numb(data)
        opr = addition(opr, 1)
        sub = addition(minuend, opr)
        sub = bin(sub)
        A[0] = sub[2:]
        

    elif opcode == 6:   #INC
        inc = addition(data, bin_one)
        if addrMode == 1 :
            registers[operand_hex] = inc
        elif addrMode == 2 :
            memo_address = registers[operand_hex]
            memo_address = int(memo_address,2)
            memo_address = memo_address[2:]
            memory[memo_address] = inc
        
    elif opcode == 7:   #DEC
        not_bin_one = not_numb(bin_one)
        dec = addition(data, not_bin_one)
        if addrMode == 1 :
            registers[operand_hex] = dec
        elif addrMode == 2 :
            memo_address = registers[operand_hex]
            memo_address = int(memo_address,2)
            memo_address = memo_address[2:]
            memory[memo_address] = dec
        
    elif opcode == 8:   #XOR
        operand1 = A[0]
        operand_xor = ""
        for i in range(len(data)) :
            if operand1[i] == data[i] :
                operand_xor = operand_xor + "0"
            else :
                operand_xor = operand_xor + "1"

    elif opcode == 9:   #AND
        operand1 = A[0]
        operand_and = ""
        for i in range(len(operand1)) :
            if (operand1[i] == "1") and (operand2[i] == "1") :
                operand_and = operand_xor + "1"
            else :
                operand_and = operand_xor + "0"

    elif opcode == 10:  #OR
        operand_or = ""
        for i in range(len(operand1)) :
            if (operand1[i] == "0") and (operand2[i] == "0") :
                operand_or = operand_xor + "0"
            else :
                operand_or = operand_xor + "1"

    elif opcode == 11:  #NOT
        for i in range(len(data)) :
            if data[i] == 1 :
                data[i] = 0
            else :
                data[i] = 1
             
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
