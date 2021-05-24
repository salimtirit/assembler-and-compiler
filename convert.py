#!/usr/bin/python

#   Examples of usage  (all arguments entered are in hex) 
#   To convert JNZ LOOP1   enter the following:   
#   ./convert.py  14  0  12
#
#   To convert PRINT C   enter the following:   
#   ./convert.py  1c  1  3
#
#   To convert LOAD 'A'   enter the following:   
#   ./convert.py 2  0 41
#
#   To convert LOAD MYDATA   enter the following:   
#   ./convert.py 2  0 2d

import sys

opcode   = int(sys.argv[1],16) 
addrmode = int(sys.argv[2],16) 
operand  = int(sys.argv[3],16) 

bopcode = format(opcode, '06b') 
baddrmode = format(addrmode, '02b') 
boperand = format(operand, '016b') 
bin = '0b' + bopcode + baddrmode + boperand 
ibin = int(bin[2:],2) ; 
instr = format(ibin, '06x') 
print (instr)
