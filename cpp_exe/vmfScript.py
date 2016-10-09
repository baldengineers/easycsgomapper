from math import *
def toVert(string_vert):
	return (int(string_vert.split(" ")[0]),int(string_vert.split(" ")[1]),int(string_vert.split(" ")[2]))

	
def crossProduct(vecta, vectb):	
	#similar to det
	#ref: wikipedia cross product
	return ( vecta[1]*vectb[2] - vecta[2]*vectb[1],  -1*(vecta[0]*vectb[2] - vecta[2]*vectb[0]),vecta[0]*vectb[1] - vecta[1]*vectb[0] )
	
	#Vect(y*v.getVectZ() - z*v.getVectY(), z*v.getVectY() - x*v.getVectZ(), x*v.getVectY() - y*v.getVectX());


	
def dotProduct(vecta, vectb):
	return vecta[0]*vectb[0] + vecta[1]*vectb[1] + vecta[2]*vectb[2] 
	#x*v.getVectX() + y*v.getVectY() + z*v.getVectZ()
	
def coplanar(planePts, point):
	#eqn of plane.
	#ref: http://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps/EquationofaPlane3Points
	ab = (planePts[1][0]-planePts[0][0], planePts[1][1]-planePts[0][1], planePts[1][2]-planePts[0][2])
	ac = (planePts[2][0]-planePts[0][0], planePts[2][1]-planePts[0][1], planePts[2][2]-planePts[0][2])
	
	#print("\n ab vect:"+str(ab)+"\n")
	#print("\n ac vect:"+str(ac)+"\n")
	
	normal = crossProduct(ab, ac)
	
	#print("\n normal:"+str(normal)+"\n")
	
	dval = (-normal[0]*planePts[1][0]) + (-normal[1]*planePts[1][1]) + (-normal[2]*planePts[1][2])
	
	#print("\n dval:"+str(dval)+"\n")
	
	if normal[0]*point[0] + normal[1]*point[1] + normal[2]*point[2] + dval == 0:
		if point != planePts[0] and point != planePts[1] and point != planePts[2]:
			#print(str(point)+"\n is coplanar with \n"+str(planePts)+"\n")
			return True
		else:
			return False
	else:
		return False
		
def findCenter(pointList):
	xtotal,ytotal,ztotal = 0,0,0
	for point in pointList:
		xtotal += point[0]
		ytotal += point[1]
		ztotal += point[2]
	return (xtotal/len(pointList), ytotal/len(pointList), ztotal/len(pointList))

	
	
def loadVMF(filename):
	vertlist = []
	fileinfo = ''
	planelist = []
	curnum = -1
	ent_list = []
	with open(filename, 'r') as f:
		vmfDataList = f.readlines()
	
	for line in vmfDataList:
		line = line.strip()
		if "solid" in line:
			planelist.append([])
			vertlist.append([])
			curnum += 1
		if "plane" in line:
			string = line.split('\" \"')[1].replace('"','').replace("(", " ").replace(")", " ")[1:-1]
			planelist[curnum].append(string.split("   "))
			for i in string.split("   "):
				vertlist[curnum].append(i)
		if "origin" in line:
			string = line.split('\" \"')[1].replace('"','').replace("\n","")
			ent_list.append(string)
	#print(vertlist)
	allverts =[]
	for sec in vertlist:
		for i in sec:
			allverts.append(toVert(i))
	totalCenter = findCenter(allverts)
	print(totalCenter)
	for ind, planelist_in in enumerate(planelist):	
		for index,plane in enumerate(planelist_in):
			a = toVert(plane[0])
			b = toVert(plane[1])
			c = toVert(plane[2])
			inNormal = crossProduct((b[0]-a[0], b[1]-a[1],b[2]-a[2]),
									(c[0]-a[0], c[1]-a[1], c[2]-a[2]))
			numplane = [a,b,c]
			numplanecopy = [a,b,c]
			for verti in vertlist:
				for vert in verti:
					vert_num = toVert(vert)
					if vert_num not in numplane:
						if vert in vertlist[ind]:
							if coplanar((a,b,c),vert_num):
								#plane.append(vert)
								numplane.append(vert_num)
			
			center = findCenter(numplane)
			#sort verts
			for i in range(len(numplane)):
				for vertex in range(1,len(numplane)):
					if dotProduct(inNormal,crossProduct((numplane[vertex-1][0]-center[0],numplane[vertex-1][1]-center[1],numplane[vertex-1][2]-center[2]),(numplane[vertex][0]-center[0],numplane[vertex][1]-center[1],numplane[vertex][2]-center[2]))) < 0:
						#numplanecopy.append(numplane[vertex])
						pass
					else:
						#print("pos")
						numplane.insert(vertex-1,numplane[vertex])
						del numplane[vertex+1]
			planelist[ind][index] = numplane
	
	with open('cpp_exe/vertfile.vf','w') as file:
		for i in planelist:
			for index,p in enumerate(i):
				fileinfo += "\n"
				for g in p:
					fileinfo += str(g).replace("(","").replace(")","").replace(",","")+"\n"
		file.write(fileinfo[1:-1])   
	fileinfo = ''
	with open('cpp_exe/origfile.vf','w') as file:
		for orig in ent_list:
			fileinfo += orig+"\n"
		file.write(fileinfo)
	with open('cpp_exe/infofile.vf','w') as file:
		file.write(str(totalCenter).replace("(","").replace(",","").replace(")",""))
