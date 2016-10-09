def toVert(string_vert):
	return (int(string_vert.split(" ")[0]),int(string_vert.split(" ")[1]),int(string_vert.split(" ")[2]))
	
def crossProduct(vecta, vectb):	
	#similar to det
	#ref: wikipedia cross product
	return ( vecta[1]*vectb[2] - vecta[2]*vectb[1], vecta[2]*vectb[1] - vecta[1]*vectb[2], vecta[0]*vectb[1] - vecta[1]*vectb[0] )
	
	#Vect(y*v.getVectZ() - z*v.getVectY(), z*v.getVectY() - x*v.getVectZ(), x*v.getVectY() - y*v.getVectX());
	
def coplanar(planePts, point):
	#eqn of plane.
	#ref: http://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps/EquationofaPlane3Points
	ab = (planePts[1][0]-planePts[0][0], planePts[1][1]-planePts[0][1], planePts[1][2]-planePts[0][2])
	ac = (planePts[2][0]-planePts[0][0], planePts[2][1]-planePts[0][1], planePts[2][2]-planePts[0][2])
	
	print("\n ab vect:"+str(ab)+"\n")
	print("\n ac vect:"+str(ac)+"\n")
	
	normal = crossProduct(ab, ac)
	
	print("\n normal:"+str(normal)+"\n")
	
	dval = -normal[0]*planePts[1][0] -normal[1]*planePts[1][1] -normal[2]*planePts[1][2]
	
	if normal[0]*point[0] + normal[1]*point[1] + normal[2]*point[2] + dval == 0:
		if point != planePts[0] and point != planePts[1] and point != planePts[2]:
			print(str(point)+"\n is coplanar with \n"+str(planePts)+"\n")
			return True
		else:
			return False
	else:
		return False
	
def loadVMF(filename):
	vertlist = []
	fileinfo = ''
	planelist = []
	with open(filename, 'r') as f:
		vmfDataList = f.readlines()
	for line in vmfDataList:
		line = line.strip()
		if "plane" in line:
			string = line.split('\" \"')[1].replace('"','').replace("(", " ").replace(")", " ")[1:-1]
			planelist.append(string.split("   "))
			for i in string.split("   "):
				vertlist.append(i)
			
	for index,plane in enumerate(planelist):
		a = toVert(plane[0])
		b = toVert(plane[1])
		c = toVert(plane[2])
		for vert in vertlist:
			vert_num = toVert(vert)
			if coplanar((a,b,c),vert_num) and vert not in plane:
				plane.append(vert)
		
	
	with open('vertfile.vf','w') as file:
		for index,i in enumerate(planelist):
			if index != 0:
				fileinfo += "\n"
			for g in i:
				fileinfo += g+"\n"
		file.write(fileinfo)   



side_list = loadVMF("vmfs/pentagon.vmf")

