def loadVMF(filename):
	vertlist = []
	fileinfo = ''
	with open(filename, 'r') as f:
		vmfDataList = f.readlines()
	for index, line in enumerate(vmfDataList):
		line = line.strip()
		if "plane" in line:
			string = line.split('\" \"')[1].replace('"','').replace("(", " ").replace(")", " ")
			for index, val in enumerate(string[1:-1].split("   ")):
				if index == 0:
					x = val.split(" ")[0]
					z = val.split(" ")[2]
				elif index == 2:
					y = val.split(" ")[1]
			fourth_point = string[1:-1].split("   ")
			fourth_point.append(x+" "+y+" "+z)
			vertlist.append(fourth_point)
			#print(vertlist)
	with open('vertfile.vf','w') as file:
		for i in vertlist:
			for g in i:
				fileinfo += g+"\n"
		file.write(fileinfo)   



side_list = loadVMF("test.vmf")

