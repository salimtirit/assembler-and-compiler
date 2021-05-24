import sys

def string_binary_to_integer(binary):
    times = len(binary)-1
    y = 0 
    for x in binary:
        y += int(x)* 2**times
        times-= 1
    return y

counter = 0   #counts instructions
all_lines = []  #store lines
registers = ["","A", "B", "C", "D"]
label_dict = {}  #stores labels with their address values, a map
opcode_list = ["", "HALT", "LOAD", "STORE", "ADD", "SUB", "INC", "DEC", "XOR", "AND", "OR", "NOT", "SHL", "SHR", "NOP", "PUSH", "POP", "CMP", "JMP", ["JZ", "JE"], ["JNZ", "JNE"], "JC", "JNC", "JA", "JAE", "JB", "JBE", "READ", "PRINT"]


inputFile = open("prog.asm", "r")
outputFile = open("prog.bin", "w")

for line in inputFile:
    line = line.strip()
    all_lines.append(line)

    if line.find(":") != -1 :  #label
        label = line.strip(":")
        label_dict[label] = counter*3   #defining the address of the label
        
    else:
        counter += 1

isLabel = False
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
        isLabel = True

    addessing_mode = ""
    #data part
    if isLabel == False :
        if instruction == "HALT":
            addessing_mode = "00"
            hex_data = "0000"
        else:
            data = tokens[1]
            if (data[0] == "[") & (data[-1] == "]") :  #address
                data = data[1:-1]  #I am starting to like python

                if registers.__contains__(data) :
                    addessing_mode = "10"   # address of data given in a register
                    hex_data = "000" + str(registers.index(data))
                else :
                    addessing_mode = "11"   # address of data is given
                    hex_data = data

            elif registers.__contains__(data) :  
                addessing_mode = "01"   # data in register
                hex_data = "000" + str(registers.index(data))

            else :
                addessing_mode = "00"  # immerdiate data
                if (data[0] == "'") & (data[-1] == "'") :
                    data = data[1:-1]
                    hex_data = hex(ord(data))
                elif label_dict.keys().__contains__(data) :
                    hex_data = hex(label_dict[data])
                elif (ord(data[0]) < 58 ) & (ord(data[0]) > 47) :
                    hex_data = data
                else:
                    data = data.strip(":")
                    hex_data = hex(label_dict[data])
            
    if isLabel == False:
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
        outputFile.write(result+"\n")

    elif instruction == "HALT" :

        result = "040000"
        outputFile.write(result+"\n")

    #else:  #label
        
    isLabel = False

outputFile.close()