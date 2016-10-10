#contains functions used for "geometry"
def crossProduct(vecta, vectb):	
	#similar to det
	#ref: wikipedia cross product
	return ( vecta[1]*vectb[2] - vecta[2]*vectb[1],  -1*(vecta[0]*vectb[2] - vecta[2]*vectb[0]),vecta[0]*vectb[1] - vecta[1]*vectb[0] )
	
def coplanar(planePts, point):
	#eqn of plane.
	#ref: http://www.maplesoft.com/support/help/Maple/view.aspx?path=MathApps/EquationofaPlane3Points
	ab = (planePts[1][0]-planePts[0][0], planePts[1][1]-planePts[0][1], planePts[1][2]-planePts[0][2])
	ac = (planePts[2][0]-planePts[0][0], planePts[2][1]-planePts[0][1], planePts[2][2]-planePts[0][2])
	
	normal = crossProduct(ab, ac)
	
	dval = (-normal[0]*planePts[1][0]) + (-normal[1]*planePts[1][1]) + (-normal[2]*planePts[1][2])
	
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
		
def sortPtsClockwise(pointList):
	#if these points are coplanar, this will work (i use this in the vmf parsing script)
	
	a = pointList[0]
	b = pointList[1]
	c = pointList[2]
	
	center = findCenter(pointList)
	
	inNormal = crossProduct((b[0]-a[0], b[1]-a[1],b[2]-a[2]),
									(c[0]-a[0], c[1]-a[1], c[2]-a[2]))
	
	for i in range(len(pointList)):
		for vertex in range(1,len(pointList)):
			if dotProduct(inNormal,crossProduct((pointList[vertex-1][0]-center[0],pointList[vertex-1][1]-center[1],pointList[vertex-1][2]-center[2]),(pointList[vertex][0]-center[0],pointList[vertex][1]-center[1],pointList[vertex][2]-center[2]))) < 0:
				#numplanecopy.append(pointList[vertex])
				pass
			else:
				#print("pos")
				pointList.insert(vertex-1,pointList[vertex])
				del pointList[vertex+1]
				
	#returns sorted list
	return pointList

def area(pts):
	#pts is a list of points with x,y values
	#area() is basically shoelace method 
	X,Y = 0,1
	return abs(sum([pts[i][X] * pts[i+1][Y] - pts[i+1][X] * pts[i][Y] for i in range(len(pts)-1)] + [pts[-1][X] * pts[0][Y] - pts[0][X] * pts[-1][Y]]) / 2)
