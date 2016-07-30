import assembly
import linking
import loading

def process(filenames, offset):
	assembly.optable = {}
	assembly.symtable = {}
	assembly.globaltable = {}
	assembly.filelen = {}
	assembly.looptable = {}
	assembly.iftable = {}
	assembly.err = False
	assembly.c_to_ass(filenames)
	if assembly.err == True:
		print("Error")
		return
	linking.filelen = assembly.filelen
	linking.globaltable = assembly.globaltable
	linking.err = False
	linking.inti_loc_file = {}
	linking.c_to_ass(filenames)
	if linking.err == True:
		print("Error")
		return
	loading.ass_to_instrctset(filenames[0], offset)

def all(fileloc, offset):
	with open(fileloc, "r") as fil:
		file_list = fil.read().split("\n")
		fil.close()
	for i in range(len(file_list)):
		file_list[i] = "/home/krishna/Assembler/docs/" + file_list[i]
	process(file_list, offset)