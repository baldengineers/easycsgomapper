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

def area(pts):
	#pts is a list of points with x,y values
	#area() is basically shoelace method 
	X,Y = 0,1
	return abs(sum([pts[i][X] * pts[i+1][Y] - pts[i+1][X] * pts[i][Y] for i in range(len(pts)-1)] + [pts[-1][X] * pts[0][Y] - pts[0][X] * pts[-1][Y]]) / 2)
