import sys
import re
inputName = sys.argv[1] # taking input   
name = re.search('\w+(?=.bin)',inputName) # taking input name using regex
outputName = "{}.txt".format(name[0]) # using "name" to name output
inputFile = open(inputName, "r") 
outputFile = open(outputName, "w")

bin_one = "0"*15+"1" # binary 16 bit one
bin_zero = "0"*16 # binary 16 bit zero
not_bin_one = "1"*16 # not of binary 16 bit one


# Registers
A = [bin_zero]
B = [bin_zero]
C = [bin_zero]
D = [bin_zero]
E = [bin_zero]
S = 2**16 - 1 # s register pointing to the last index of memory array
PC = 0 # program counter starting from zeroth index
CF = 0 # carry flag zero or one throughout the program to directly use
ZF = False # zero flag boolean
SF = False # sign flag boolean

memory = ["0"*8] * 2**16 # memory of our computer 64K

registers = {
    "0000" : PC,
    "0001" : A,
    "0002" : B,
    "0003" : C,
    "0004" : D,
    "0005" : E,
    "0006" : S
}

# adjusting ZF and SF after an operation checking data
# if data is binary zero ZF becomes true, becomes false otherwise
# if data starts with a "1" this means data is negative so SF is true, otherwise SF is false
def adjust_flag(data) :
    global ZF
    global SF
    if data == bin_zero :    # adjust ZF
        ZF = True
    else :
        ZF = False

    if data[0] == "1" :  # adjust SF
        SF = True     
    else :
        SF = False

# taking the not of a number (this is not twos complement just not)
def not_numb(data) :
    return_data = ""
    for i in data :
        if i == "1" :
            return_data = return_data + "0"
        else :
            return_data = return_data + "1"
    return return_data

# adding (also subtracting in a way) two numbers
def addition (data, addend):
    i = len(data) - 1
    sum = ""
    global CF
    CF = 0
    while i >= 0 :    
        temp = int(data[i]) + int(addend[i]) + CF
        if temp > 1 : 
            CF = 1
            sum = str(temp-2) + sum
        else :
            CF = 0
            sum = str(temp) + sum 
        i -= 1
    
    adjust_flag(sum)
    return sum

# main part of the program reading the input file line by line
for line in inputFile:
    line = bin(int(line,16))   # hex value to binary
    line = str(line)
    line = line[2:]  # deleting '0b' part 
    line = line.zfill(24) # adding missing '0's
    memory[PC] = line[0:8]  # loading them to memory
    PC+=1
    memory[PC] = line[8:16] # first part of the operand
    PC+=1
    memory[PC] = line[16:] # second part of the operand
    PC+=1

lastInstruction = PC
PC = 0

# executing all instructions one by one
while PC <= lastInstruction:
    instruction  = memory[PC]
    opcode = instruction[0:6] # taking opcode
    opcode = int(opcode,2)

    addrMode = instruction[6:] #taking addressing mode
    addrMode = int(addrMode,2)

    PC += 1
    operand1 = memory[PC] #taking operands
    PC += 1
    operand2 = memory[PC] 
    operand = str(operand1) + str(operand2)

    operand_hex = hex(int(operand,2)) #changing operand to hex value
    operand_hex = operand_hex[2:]
    operand_hex =  operand_hex.zfill(4)

    #taking the data
    if addrMode == 0 :
        data  = operand
    elif addrMode == 1 :
        data = registers[operand_hex][0]
    elif addrMode == 2 :
        memo_address = registers[operand_hex][0]
        memo_address = int(memo_address,2)
        if opcode != 3: # to not try taking unexisting data
            data = memory[memo_address] + memory[memo_address+1]
    else :
        memo_address = int(operand,2)
        data = memory[memo_address] + memory[memo_address+1] 


    if opcode == 1:  # HALT
        break
    elif opcode == 2: # LOAD
        A[0] = data
    elif opcode == 3:   # STORE
        if addrMode == 1 : # register is given
            registers[operand_hex][0] = A[0]
        elif addrMode == 2 :
            memory[memo_address] = A[0][:8]
            memory[memo_address + 1] = A[0][8:]

    elif opcode == 4:   # ADD
        sum = addition(data, A[0])
        A[0] = sum

    elif opcode == 5:   # SUB
        operand = not_numb(data)
        operand = addition(operand, bin_one)
        sub = addition(A[0], operand)
        A[0] = sub
        
    elif opcode == 6:   # INC
        inc = addition(data, bin_one)
        if addrMode == 1 :
            registers[operand_hex][0] = inc
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = inc[:8]
            memory[memo_address + 1] = inc[8:]
        
    elif opcode == 7:   # DEC
        dec = addition(data, not_bin_one)
        if addrMode == 1 :
            registers[operand_hex][0] = dec
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = dec[:8]
            memory[memo_address + 1] = dec[8:]
        
    elif opcode == 8:   # XOR
        xor = ""
        for i in range(len(data)) :
            if A[0][i] == data[i] :
                xor = xor + "0"
            else :
                xor = xor + "1"

        adjust_flag(xor)
        A[0] = xor

    elif opcode == 9:   # AND
        operand_and = ""
        for i in range(len(data)) :
            if (A[0][i] == "1") and (data[i] == "1") :
                operand_and = operand_and + "1"
            else :
                operand_and = operand_and + "0"

        adjust_flag(operand_and)
        A[0] = operand_and

    elif opcode == 10:  # OR
        operand_or = ""
        for i in range(len(data)) :
            if (A[0][i] == "0") and (data[i] == "0") :
                operand_or = operand_or + "0"
            else :
                operand_or = operand_or + "1"

        adjust_flag(operand_or)
        A[0] = operand_or

    elif opcode == 11:  # NOT
        operand_not = not_numb(data)
        if addrMode == 1 :
            registers[operand_hex][0] = operand_not
        elif addrMode == 2 or addrMode == 3 :
            memory[memo_address] = operand_not[:8]
            memory[memo_address + 1] = operand_not[8:]
             
    elif opcode == 12:  # SHL
        data = data[1:] + "0"
        registers[operand_hex][0] = data

    elif opcode == 13:  # SHR
        data = "0" + data[:-1]
        registers[operand_hex][0] = data

    elif opcode == 15:  # PUSH
        memory[S] = data[:8]
        S -= 1
        memory[S] = data[8:]
        S -= 1

    elif opcode == 16:  # POP
        registers[operand_hex][0] = memory[S+2] + memory[S+1]
        S += 2 

    elif opcode == 17:  # CMP
        operand = not_numb(data)
        operand = addition(operand, bin_one)
        addition(A[0],operand)
    elif opcode == 18: # JMP
        PC = int(data,2)-1
    elif opcode == 19: # JZ JE
        if ZF:
            PC = int(data,2)-1
    elif opcode == 20: # JNZ JNE
        if not(ZF):
            PC = int(data,2)-1
    elif opcode == 21: # JC
        if CF == 1:
            PC = int(data,2)-1
    elif opcode == 22: # JNC
        if CF == 0:
            PC = int(data,2)-1
    elif opcode == 23: # JA
        if not(SF) and not(ZF):
            PC = int(data,2)-1
    elif opcode == 24: # JAE
        if not(SF):
            PC = int(data,2)-1
    elif opcode == 25: # JB
        if SF:
            PC = int(data,2)-1
    elif opcode == 26: # JBE
        if SF or ZF:
            PC = int(data,2)-1
    elif opcode == 27: # READ
        inputs = input()
        inputs = inputs[0]
        inputs = (str(bin(ord(inputs)))[2:]).zfill(16) # changing char to bin to string to remove 0b from beginning and completing to 16 bits
        if addrMode == 1:
            registers[operand_hex][0] = inputs
        elif addrMode == 2:
            memo_address = registers[operand_hex][0]
            memo_address = int(memo_address,2)
            memory[memo_address] = inputs[:8]
            memory[memo_address+1] = inputs[8:]
        elif addrMode == 3:
            memo_address = int(operand,2)
            memory[memo_address] = inputs[:8]
            memory[memo_address+1] = inputs[8:]
    elif opcode == 28: # PRINT
        outputFile.write(chr(int(data,2))+"\n")
    PC += 1

outputFile.close()