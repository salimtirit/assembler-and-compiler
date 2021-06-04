import sys
import re
def string_binary_to_integer(binary):
    times = len(binary)-1
    y = 0 
    for x in binary:
        y += int(x)* 2**times
        times-= 1
    return y

def valid_hex(data) :

    if len(data) == 4 :
        for x in range(4) :
            val = ord(data[x])
            if not (( val > 47 and val < 58 ) or ( val > 96 and val < 103 ) or ( val > 64 and val < 71 )) : # not in [0-9a-fA-F] range
                exit(0)
    else :
        exit(0)
    return True

counter = 0   #counts instructions
all_lines = []  #store lines
registers = ["","A", "B", "C", "D", "E"]
label_dict = {}  #stores labels with their address values, a map
opcode_list = ["", "HALT", "LOAD", "STORE", "ADD", "SUB", "INC", "DEC", "XOR", "AND", "OR", "NOT", "SHL", "SHR", "NOP", "PUSH", "POP", "CMP", "JMP", "JZ", "JNZ", "JC", "JNC", "JA", "JAE", "JB", "JBE", "READ", "PRINT","JE","JNE"]
valid_addModes = [[],[0,1,2,3],[0,1,2,3],[1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[1,2],[1,2],[0,1,2,3],[1,2],[1,2],[0,1,2,3],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1,2,3],[0,1,2,3],[0],[0]]
output_queue = []

sayi = sys.argv[1]
name = "./230-p2-testcases/input{}.asm".format(sayi)
name2 = "output{}.bin".format(sayi)
inputFile = open(name, "r")

for line in inputFile:
    line = line.strip()
    if line == "":
        continue
    all_lines.append(line)

    if not(line.__contains__(" ")) :  #no white space means that there is only one token which is label or HALT or NOP 
        if line.find(":") != -1 :  #label
            label = line.strip(":")
            label_dict[label] = counter*3   #defining the address of the label
        elif line == "HALT" or line == "NOP" :
            counter += 1
        else :  #invalid instruction
            exit(0)
        
    else:
        counter += 1

noSecond = False
for lines in all_lines:
    tokens = lines.split(" ") #pattern tokens = line.split() de olur
    instruction = tokens[0]
    opcode = ""
    #opcode part
    if instruction == "JZ" or instruction == "JE" :
        opcode = bin(19)
    elif instruction == "JNZ" or instruction == "JNE" :
        opcode = bin(20)
    elif opcode_list.__contains__(instruction) :
        opcode = bin(opcode_list.index(instruction))
    else: 
        if label_dict.keys().__contains__(instruction[:-1]) :
            noSecond = True
        else :  #invalid instruction this part might be not necessary
            exit(0)     

    addessing_mode = ""
    #data part
    if noSecond == False :
        index = opcode_list.index(instruction)
        valid_addr_modes = valid_addModes[index]

        if instruction == "HALT" or instruction == "NOP":
            addessing_mode = "00"
            hex_data = "0x0000"
            if len(tokens) > 1 :
                exit(0) 
        else:
            if len(tokens) == 1 :  # means there is a valid instruction without given data
                exit(0)
            data = tokens[1]
            if (data[0] == "[") & (data[-1] == "]") :  #address
                data = data[1:-1]  #I am starting to like python
                if registers.__contains__(data) :
                    if not valid_addr_modes.__contains__(2) :
                        exit(0)
                    addessing_mode = "10"   # address of data given in a register
                    hex_data = "0x000" + str(registers.index(data)) 
                else :
                    if not valid_addr_modes.__contains__(3) :
                        exit(0)
                    addessing_mode = "11"   # address of data is given
                    valid_hex(data) 
                    hex_data = "0x" + data

            elif registers.__contains__(data) :  
                if not valid_addr_modes.__contains__(1) :
                    exit(0)
                addessing_mode = "01"   # data in register
                hex_data = "0x000" + str(registers.index(data))

            else :
                addessing_mode = "00"  # immerdiate data
                if (data[0] == "'") & (data[-1] == "'") :  #char is given
                    if not valid_addr_modes.__contains__(0) :
                        exit(0)
                    data = data[1:-1]
                    if len(data) != 1 :
                        exit(0)
                    hex_data = hex(ord(data))
                elif label_dict.keys().__contains__(data) : #label
                    hex_data = hex(label_dict[data])
                #elif data.find(":") != -1 :  #?
                #   data = data.strip(":")
                #    hex_data = hex(label_dict[data])
                else :  
                    hex_data = "0x"+data
              
                    
            
    if noSecond == False :
        opcode = str(opcode)
        first_two = opcode[2:] + str(addessing_mode)

        a = hex(string_binary_to_integer(first_two))
        a = str(a)[2:]
        while len(a) < 2:
            a = "0" + a

        hex_data = str(hex_data)[2:]
        while len(hex_data) < 4:
            hex_data = "0" + hex_data

        result =  a + hex_data
        output_queue.append(result+"\n")

    elif instruction == "HALT" :
        result = "040000"
        output_queue.append(result+"\n")

    elif instruction == "NOP":
        result = "380000"
        output_queue.append(result+"\n")

    noSecond = False

outputFile = open(name2, "w")
for lines in output_queue :
    outputFile.write(lines)  
outputFile.close()
