def ass_to_instrctset(filename, offset):
	with open(filename.split('.')[0] + '.semi', 'r') as file:
		lines = file.read().split('\n')
		file.close()

	assmbl_arr = []

	for line in lines:
		if '#' in line:
			add = int(line.split('#')[1])
			add = str(add + offset)
			line = line.replace('#' + line.split('#')[1], add)
			assmbl_arr.append(line)
		else:
			assmbl_arr.append(line)

	assmbl_arr.append('HLT')

	with open(filename.split('.')[0] + '.final', 'w') as file:
		file.write('\n'.join(assmbl_arr))
		file.close()