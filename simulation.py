registers = {'PC': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
loopstack = []
comp = False
memory = {}
lenopcode = {}
instrcution = {}

def findoptable():
	with open("/home/krishna/Assembler/bin/new/codes.cf", "r") as file:
		codes = file.read().split("\n")
		file.close()
	for opcode in codes:
		opcode = opcode.lstrip().rstrip()
		if opcode != '':
			lenopcode[opcode.split()[0]] = int(opcode.split()[1])

def initiate(lines, offset):
	memadd = offset
	registers['PC'] = offset
	for line in lines:
		opcode = line.split(' ')[0]
		if opcode == 'DB':
			memory[memadd] = int(line.split(' ')[1])
			memadd = memadd + 1
		else:
			instrcution[memadd] = line
			memadd = memadd + lenopcode[opcode]

def process(instr):
	opcode = instr.split(' ')[0]
	if opcode == 'JMP':
		registers['PC'] = int(instr.split(' ')[1])
	elif opcode == 'LDA':
		registers['A'] = memory[int(instr.split(' ')[1])]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'STA':
		memory[int(instr.split(' ')[1])] = registers['A']
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'MVI':
		ops = instr.split(' ')[1]
		registers[ops.split(',')[0]] = int(ops.split(',')[1])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ADI':
		registers['A'] = registers['A'] + int(instr.split(' ')[1])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'MOV':
		vari = instr.split(' ')[1]
		var1, var2 = vari.split(',')
		registers[var1] = registers[var2]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ADD':
		registers['A'] = registers['A'] + registers[instr.split(' ')[1]]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'SUI':
		registers['A'] = registers['A'] - int(instr.split(' ')[1])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'SUB':
		registers['A'] = registers['A'] - registers[(instr.split(' ')[1])]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ANI':
		registers['A'] = registers['A'] & int(instr.split(' ')[1])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ANA':
		registers['A'] = registers['A'] & registers[instr.split(' ')[1]]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ORI':
		registers['A'] = registers['A'] | int(instr.split(' ')[1])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'ORA':
		registers['A'] = registers['A'] | registers[instr.split(' ')[1]]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'PUSH':
		loopstack.append(registers[instr.split(' ')[1]])
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'JNZ':
		if registers['A'] != 0:
			registers['PC'] = int(instr.split(' ')[1])
		else:
			registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'POP':
		registers[instr.split(' ')[1]] = loopstack[len(loopstack) - 1]
		loopstack = loopstack[:len(loopstack) - 1]
		registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'JP':
		if registers['A'] > 0:
			registers['PC'] = int(instr.split(' ')[1])
		else:
			registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'JZ':
		if registers['A'] == 0:
			registers['PC'] = int(instr.split(' ')[1])
		else:
			registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'JM':
		if registers['A'] < 0:
			registers['PC'] = int(instr.split(' ')[1])
		else:
			registers['PC'] = registers['PC'] + lenopcode[opcode]
	elif opcode == 'HLT':
		global comp
		comp = True

def simulation(filename, offset):
	global comp
	global registers
	global loopstack
	global comp
	global memory
	global lenopcode
	global instrcution
	registers = {'PC': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
	loopstack = []
	comp = False
	memory = {}
	lenopcode = {}
	instrcution = {}
	comp = False
	findoptable()
	with open(filename.split('.')[0] + '.final', 'r') as file:
		lines = file.read().split('\n')
	initiate(lines, offset)