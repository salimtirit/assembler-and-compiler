import sys

def decimal_to_binary(decimal):

    binary = ""
    while (decimal != 0):

        remainder = decimal%2
        binary = str(remainder) + binary        
        decimal //= 2

    return binary


def decimal_to_hex(decimal):

    hex = ""
    while (decimal != 0):

        remainder = decimal % 16
        if remainder > 9:
            remainder = chr(55+remainder)

        hex = str(remainder) + hex        
        decimal //= 16

    return hex

counter = 0   #counts instructions
all_lines = []  #store lines
registers = ["","A", "B", "C", "D"]
label_dict = {}  #stores labels with their address values, a map
opcode_list = ["", "HALT", "LOAD", "STORE", "ADD", "SUB", "INC", "DEC", "XOR", "AND", "OR", "NOT", "SHL", "SHR", "NOP", "PUSH", "POP", "CMP", "JMP", ["JZ", "JE"], ["JNZ", "JNE"], "JC", "JNC", "JA", "JAE", "JB", "JBE", "READ", "PRINT"]


inputFile = open("prog.asm", "r")

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
    tokens = line.split(" ") #pattern tokens = line.split() de olur
    instruction = tokens[0]
    data = tokens[1]

    #opcode part
    if instruction == "JZ" | instruction == "JE" :
        opcode = "10011"
    elif instruction == "JNZ" | instruction == "JNE" :
        opcode = "10100"
    elif opcode_list.__contains__(opcode) :
        opcode = decimal_to_binary(opcode_list.index(instruction))
    else: 
        isLabel = True

    #data part
    if isLabel == False :

        if data[0] == "[" & data[-1] == "]" :  #address
            inner_data = data[1:-1]  #I am starting to like python

            if registers.__contains__(inner_data) :
                addessing_mode = "10"   # address of data given in a register
                hex_data = "000" + registers.index(data)
            else :
                addessing_mode = "11"   # address of data is given
                hex_data = data

        elif registers.__contains__(data) :  
            addessing_mode = "01"   # data in register
            hex_data = "000" + registers.index(data)

        else :
            addessing_mode = "00"  # immerdiate data

            if data[0] == "'" & data[-1] == "'" :
                hex_data = decimal_to_hex(ord(data))
            elif label_dict.keys().__contains__(data) :
                hex_data = decimal_to_hex(label_dict[data])
            else :
                hex_data = data
            

    isLabel = False