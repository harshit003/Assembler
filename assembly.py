import re

optable = {}
symtable = {}
globaltable = {}
filelen = {}
looptable = {}
iftable = {}
err = False

def optablestore():
	with open("/home/krishna/Assembler/bin/new/codes.cf", "r") as file:
		codes = file.read().split("\n")
		file.close()
	for opcode in codes:
		opcode = opcode.lstrip().rstrip()
		if opcode != '':
			optable[opcode.split()[0]] = int(opcode.split()[1])

def checkint(string):
	try:
		int(string)
		return True
	except:
		return False

def c_to_ass(filenames):
	global err
	optablestore()
	variable = re.compile("var\s+(\w+)\s*=\s*(\w+)\s*")
	glbl = re.compile("global\s+var\s+(\w+)\s*=\s*(\w+)\s*")
	extern = re.compile("extern\svar\s+(\w+)\s*")
	plus  = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)\s*")
	minus = re.compile("\s*(\w+)\s*=\s*(\w+)\s*-\s*(\w+)\s*")
	nd = re.compile("\s*(\w+)\s*=\s*(\w+)\s*&\s*(\w+)\s*")
	ur = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\|\s*(\w+)\s*")
	ifgrthan = re.compile("\s*if\s+(\w+)\s*>\s*(\w+)\s*")
	iflessthan = re.compile("\s*if\s+(\w+)\s*<\s*(\w+)\s*")
	ifeqto = re.compile("\s*if\s+(\w+)\s*=\s*(\w+)\s*")
	ifend = re.compile("\s*endif\s*")
	loop = re.compile("\s*loop\s+(\w+)\s*")
	endloop = re.compile("\s*endloop\s*")
	multi = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s*")
	div = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\/\s*(\w+)\s*")
	minimum = re.compile("\s*(\w+)\s*=\s*min\s*\((.*)\)\s*")
	maximum = re.compile("\s*(\w+)\s*=\s*max\s*\((.*)\)\s*")
	for filenam in filenames:
		with open(filenam, 'r') as file:
			code = file.read()
			lines = code.split('\n')
			file.close()

		filename = filenam.split('.')[0]	

		memadd = 0
		loops = 0		
		ifs = 0
		symtable[filename] = {}
		globaltable[filename] = {}
		assmbl_arr = []
		looptable = {}
		iftable = {}

		for line in lines :
			line = line.lstrip().rstrip()

			if glbl.match(line):
				var1 = glbl.match(line).group(1)
				var2 = glbl.match(line).group(2) 
				if((not  checkint(var2) and var2 not in symtable[filename]) or checkint(var1)):
					err = True
					return
				if checkint(var2):
					assmbl_arr.append("JMP #" + str(memadd + 4))
					assmbl_arr.append("DB " + str(var2))
					symtable[filename][var1] = "#" + str(memadd + 3)
					globaltable[filename][var1] = "#" + str(memadd + 3)
					memadd = memadd + optable["JMP"] + 1
				else:
					assmbl_arr.append("JMP #" + str(memadd + 4))
					symtable[filename][var1] = "#" + str(memadd + 3)
					globaltable[filename][var1] = "#" + str(memadd + 3)
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["JMP"] + optable["LDA"] + optable["STA"] + 1
			elif variable.match(line):
				var1 = variable.match(line).group(1)
				var2 = variable.match(line).group(2)
				if (not checkint(var2) and var2 not in symtable[filename]) or checkint(var1):
					err = True
					return
				if checkint(var2):
					assmbl_arr.append("JMP #" + str(memadd + 4))
					assmbl_arr.append("DB " + str(var2))
					symtable[filename][var1] = "#" + str(memadd + 3)
					memadd = memadd + optable["JMP"] + 1
				else:
					assmbl_arr.append("JMP #" + str(memadd + 4))
					symtable[filename][var1] = "#" + str(memadd + 3)
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["JMP"] + optable["LDA"] + optable["STA"] + 1
			elif extern.match(line):
				var = extern.match(line).group(1)
				if checkint(var):
					err = True
					return
				symtable[filename][var] = "$" + str(var)
			elif plus.match(line):
				var1 = plus.match(line).group(1)
				var2 = plus.match(line).group(2)
				var3 = plus.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = True
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("ADI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ADI"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ADI " + str(var2))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ADI"] + optable["STA"]
				elif checkint(var3):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("ADI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ADI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ADD B")
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["STA"]
			elif minus.match(line):
				var1 = minus.match(line).group(1)
				var2 = minus.match(line).group(2)
				var3 = minus.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = True
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("SUI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("SUB B")
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["MVI"] + optable["SUB"] + optable["STA"]
				elif checkint(var3):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("SUI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("SUB B")
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["STA"]
			elif nd.match(line):
				var1 = nd.match(line).group(1)
				var2 = nd.match(line).group(2)
				var3 = nd.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = True
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("ANI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ANI"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ANI " + str(var2))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ANI"] + optable["STA"]
				elif checkint(var3):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("ANI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ANI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ANA B")
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ANA"] + optable["STA"]
			elif ur.match(line):
				var1 = ur.match(line).group(1)
				var2 = ur.match(line).group(2)
				var3 = ur.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = True
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("ORI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ORI"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ORI " + str(var2))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ORI"] + optable["STA"]
				elif checkint(var3):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("ORI " + str(var3))
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ORI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + str(symtable[filename][var2]))
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + str(symtable[filename][var3]))
					assmbl_arr.append("ORA B")
					assmbl_arr.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ORA"] + optable["STA"]
			elif loop.match(line):
				var1 = loop.match(line).group(1)

				if not checkint(var1) and var1 not in symtable[filename][var1]:
					err = True
					return
				if checkint(var1):
					assmbl_arr.append("PUSH E")
					assmbl_arr.append("MVI E," + str(var1))
					memadd = memadd + optable["PUSH"] + optable["MVI"]
					looptable[loops] = "#" + str(memadd)
					loops = loops + 1
				else:
					assmbl_arr.append("PUSH E")
					assmbl_arr.append("LDA " + str(symtable[filename][var1]))
					assmbl_arr.append("MOV E,A")
					memadd = memadd + optable["PUSH"] + optable["LDA"] + optable["MOV"]
					looptable[loops] = "#" + str(memadd)
					loops = loops + 1
			elif endloop.match(line):
				if loops == 0:
					err = True
					return
				assmbl_arr.append("MOV A,E")
				assmbl_arr.append("SUI 1")
				assmbl_arr.append("MOV E,A")
				assmbl_arr.append("JNZ " + looptable[loops - 1])
				loops = loops - 1
				assmbl_arr.append("POP E")
				memadd = memadd + optable["MOV"] + optable["SUI"] + optable["MOV"] + optable["JNZ"] + optable["POP"]
			elif multi.match(line):
				var1 = multi.match(line).group(1)
				var2 = multi.match(line).group(2)
				var3 = multi.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = "Invalid line: " + line
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI B,0")
					assmbl_arr.append("MVI A," + str(var3))
					memadd = memadd + optable["MVI"] + optable["MVI"]
					assmbl_arr.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("ADD B")
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("SUI 1")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,B")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = "Invalid line: " + line
						return
					assmbl_arr.append("MVI B,0")
					assmbl_arr.append("LDA " + symtable[filename][var3])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					assmbl_arr.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("ADD B")
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("SUI 1")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,B")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif checkint(var3):
					if var2 not in symtable[filename]:
						err = "Invalid line: " + line
						return
					assmbl_arr.append("MVI B,0")
					assmbl_arr.append("LDA " + symtable[filename][var2])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					assmbl_arr.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("MVI A," + str(var3))
					assmbl_arr.append("ADD B")
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("SUI 1")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,B")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						err = "Invalid line: " + line
						return
					assmbl_arr.append("MVI B,0")
					assmbl_arr.append("LDA " + symtable[filename][var2])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					assmbl_arr.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("LDA " + symtable[filename][var3])
					assmbl_arr.append("ADD B")
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("SUI 1")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,B")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
			elif div.match(line):
				var1 = div.match(line).group(1)
				var2 = div.match(line).group(2)
				var3 = div.match(line).group(3)
				if checkint(var1) or var1 not in symtable[filename]:
					err = "Invalid line: " + line
					return
				if checkint(var2) and checkint(var3):
					assmbl_arr.append("MVI B," + str(var3))
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("SUB B")
					assmbl_arr.append("MVI C,0")
					memadd = memadd + optable["MVI"] + optable["MVI"] + optable["SUB"] + optable["MVI"]
					assmbl_arr.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					assmbl_arr.append("MOV F,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("ADI 1")
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("MOV A,F")
					assmbl_arr.append("SUB B")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif checkint(var2):
					if var3 not in symtable[filename]:
						err = "Invalid line: " + line
						return
					assmbl_arr.append("LDA " + symtable[filename][var3])
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("MVI A," + str(var2))
					assmbl_arr.append("SUB B")
					assmbl_arr.append("MVI C,0")
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["MVI"] + optable["SUB"] + optable["MVI"]
					assmbl_arr.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					assmbl_arr.append("MOV F,A")
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("ADI 1")
					assmbl_arr.append("MOV C,A")
					assmbl_arr.append("MOV A,F")
					assmbl_arr.append("SUB B")
					assmbl_arr.append("JMP #" + str(memadd))
					assmbl_arr.append("MOV A,C")
					assmbl_arr.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
			elif minimum.match(line):
				var1 = minimum.match(line).group(1)
				vas = minimum.match(line).group(2)
				if checkint(var1) or var1 not in symtable[filename]:
					err = "Invalid line: " + line
					return
				vas = vas.split(',')
				for i in range(len(vas)):
					vas[i] = vas[i].lstrip().rstrip()
				if checkint(vas[0]):
					assmbl_arr.append("MVI A," + str(vas[0]))
					memadd = memadd + optable["MVI"]
				elif vas[0] not in symtable[filename]:
					err = "Invalid line: " + line
				else:
					assmbl_arr.append("LDA " + symtable[filename][vas[0]])
					memadd = memadd + optable["LDA"]
				vas = vas[1:]
				for var in vas:
					if checkint(var):
						assmbl_arr.append("MVI B," + str(var))
						assmbl_arr.append("MOV C,A")
						assmbl_arr.append("SUB B")
						memadd = memadd + optable["MVI"] + optable["MOV"] + optable["SUB"]
						assmbl_arr.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"]))
						assmbl_arr.append("MOV G,B")
						assmbl_arr.append("JP #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"]))
						assmbl_arr.append("MOV G,C")
						assmbl_arr.append("MOV A,G")
						memadd = memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"] + optable['MOV']
					elif var not in symtable[filename]:
						err = "Invalid line: " + line
						return
					else:
						assmbl_arr.append("MOV C,A")
						assmbl_arr.append("LDA " + symtable[filename][var])
						assmbl_arr.append("MOV B,A")
						assmbl_arr.append("MOV A,C")
						assmbl_arr.append("SUB B")
						memadd = memadd + optable["MOV"] + optable["LDA"] + optable["MOV"] + optable["MOV"] + optable["SUB"]
						assmbl_arr.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"]))
						assmbl_arr.append("MOV G,B")
						assmbl_arr.append("JP #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"]))
						assmbl_arr.append("MOV G,C")
						assmbl_arr.append("MOV A,G")
						memadd = memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"] + optable['MOV']
				assmbl_arr.append("STA " + symtable[filename][var1])
				memadd = memadd + optable["STA"]
			elif maximum.match(line):
				var1 = maximum.match(line).group(1)
				vas = maximum.match(line).group(2)
				if checkint(var1) or var1 not in symtable[filename]:
					err = "Invalid line: " + line
					return
				vas = vas.split(',')
				for i in range(len(vas)):
					vas[i] = vas[i].lstrip().rstrip()
				if checkint(vas[0]):
					assmbl_arr.append("MVI A," + str(vas[0]))
					memadd = memadd + optable["MVI"]
				elif vas[0] not in symtable[filename]:
					err = "Invalid line: " + line
				else:
					assmbl_arr.append("LDA " + symtable[filename][vas[0]])
					memadd = memadd + optable["LDA"]
				vas = vas[1:]
				for var in vas:
					if checkint(var):
						assmbl_arr.append("MVI B," + str(var))
						assmbl_arr.append("MOV C,A")
						assmbl_arr.append("SUB B")
						memadd = memadd + optable["MVI"] + optable["MOV"] + optable["SUB"]
						assmbl_arr.append("JP #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"]))
						assmbl_arr.append("MOV G,B")
						assmbl_arr.append("JM #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"]))
						assmbl_arr.append("MOV G,C")
						assmbl_arr.append("MOV A,G")
						memadd = memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"] + optable["MOV"]
					elif var not in symtable[filename]:
						err = "Invalid line: " + line
						return
					else:
						assmbl_arr.append("MOV C,A")
						assmbl_arr.append("LDA " + symtable[filename][var])
						assmbl_arr.append("MOV B,A")
						assmbl_arr.append("MOV A,C")
						assmbl_arr.append("SUB B")
						memadd = memadd + optable["MOV"] + optable["LDA"] + optable["MOV"] + optable["MOV"] + optable["SUB"]
						assmbl_arr.append("JP #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"]))
						assmbl_arr.append("MOV G,B")
						assmbl_arr.append("JM #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"]))
						assmbl_arr.append("MOV G,C")
						assmbl_arr.append("MOV A,G")
						memadd = memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"] + optable["MOV"]
				assmbl_arr.append("STA " + symtable[filename][var1])
				memadd = memadd + optable["STA"]
			elif iflessthan.match(line):
				var1 = iflessthan.match(line).group(1)
				var2 = iflessthan.match(line).group(2)

				if checkint(var1) and checkint(var2):
					assmbl_arr.append("MVI A," + str(var1))
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JP &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				elif checkint(var1):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("SUI " + str(var1))
					assmbl_arr.append("JM &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				elif checkint(var2):
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JP &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				else:
					if var2 not in symtable[filename]:
						err = True
						return
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUB B")
					assmbl_arr.append("JP &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JP"] + optable["JZ"]
			elif ifgrthan.match(line):
				var1 = ifgrthan.match(line).group(1)
				var2 = ifgrthan.match(line).group(2)

				if checkint(var1) and checkint(var2):
					assmbl_arr.append("MVI A," + str(var1))
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JM &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				elif checkint(var1):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("SUI " + str(var1))
					assmbl_arr.append("JP &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				elif checkint(var2):
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JM &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				else:
					if var2 not in symtable[filename]:
						err = True
						return
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUB B")
					assmbl_arr.append("JM &&&" + str(ifs))
					assmbl_arr.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JM"] + optable["JZ"]
			elif ifeqto.match(line):
				var1 = ifeqto.match(line).group(1)
				var2 = ifeqto.match(line).group(2)

				if checkint(var1) and checkint(var2):
					assmbl_arr.append("MVI A," + str(var1))
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JNZ"]
				elif checkint(var1):
					if var2 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("SUI " + str(var1))
					assmbl_arr.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JNZ"]
				elif checkint(var2):
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUI " + str(var2))
					assmbl_arr.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JNZ"]
				else:
					if var2 not in symtable[filename]:
						err = True
						return
					if var1 not in symtable[filename]:
						err = True
						return
					assmbl_arr.append("LDA " + symtable[filename][var2])
					assmbl_arr.append("MOV B,A")
					assmbl_arr.append("LDA " + symtable[filename][var1])
					assmbl_arr.append("SUB B")
					assmbl_arr.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JNZ"]
			elif ifend.match(line):
				iftable[ifs - 1] = memadd
			elif line.lstrip().rstrip() != "":
				err = True
				return
		filelen[filename] = memadd

		assc = '\n'.join(assmbl_arr)
		with open(filename.split('.')[0] + '.pass1', 'w') as file:
			file.write(assc)
			file.close()

		ass_arr = []

		for line in assmbl_arr:
			if "&&&" not in line:
				ass_arr.append(line)
			else:
				ifp = line.split("&&&")[1]
				ifp = int(ifp)
				line = line.replace("&&&"+line.split("&&&")[1], "#" + str(iftable[ifp]))
				ass_arr.append(line)

		assc = '\n'.join(ass_arr)
		with open(filename.split('.')[0] + '.pass2', 'w') as file:
			file.write(assc)
			file.close()
