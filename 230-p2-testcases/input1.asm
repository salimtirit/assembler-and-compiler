	LOAD 0010
	STORE E
	LOAD 'A'
	STORE D
	LOAD 'C'
	STORE C
	SUB D
	CMP E
	JZ LABEL1
	NOP
	JNZ LABEL2
LABEL1:  
	PRINT D 
	PRINT C
LABEL2:
	PRINT D
	INC D
	DEC C
	PRINT D
	DEC D
	PRINT C
	DEC C
	PRINT C
	HALT
