import assembly

err = False
inti_loc_file = {}
filelen = assembly.filelen
globaltable = assembly.globaltable

def findlocation(string, files):
	for file in files:
		if string in globaltable[file.split('.')[0]]:
			return file.split('.')[0], globaltable[file.split('.')[0]][string].split("#")[1]
	return "val absent", "-1"

def c_to_ass(fileNames):
	global err
	memadd = 0
	for filename in fileNames:
		inti_loc_file[filename.split('.')[0]] = memadd
		memadd = memadd + filelen[filename.split('.')[0]]

	assmbl_arr = []

	for filenam in fileNames:
		filename = filenam.split('.')[0]
		with open(filename + '.pass2', 'r') as file:
			lines = file.read().split('\n')
			file.close()

		for line in lines:
			if '$' not in line and '#' not in line:
				assmbl_arr.append(line)
			elif '$' not in line:
				addr = line.split('#')[1]
				addr = str(int(addr) + inti_loc_file[filename])
				line = line.replace('#' + line.split('#')[1], '#' + addr)
				assmbl_arr.append(line)
			else:
				fname, add = findlocation(line.split('$')[1], fileNames)
				if fname == "val absent":
					err = True
					return
				line = line.replace('$' + line.split('$')[1], "#" + str(int(add) + inti_loc_file[fname]))
				assmbl_arr.append(line)

	with open(fileNames[0].split('.')[0] + '.semi', 'w') as file:
		file.write("\n".join(assmbl_arr))
		file.close()