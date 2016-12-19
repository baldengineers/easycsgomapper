#contains functions for prefab files
class Prefab():
    def __init__(self, p=[None, None, None, None, None, None]):
        self.text = p[0]
        self.section = p[1]
        self.p_vals_list = p[2]
        self.vmf_data = p[3]
        self.draw_list = p[4]
        self.color_list = p[5]

    def create(self, x, y, scale, rot):
        X,Y,Z = 0,1,2
        for i, p in enumerate(self.p_vals_list):
            xy = int(self.rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+p[X], posy*-1*scale+p[Y]), (360 if rot!=0 else 0)-90*rot))
            x = xy[X]
            y = xy[Y]
            z = p[Z]
            self.vmf_data = self.vmf_data.replace("x%d y%d z%d" % (i, i, i), "%d %d %d" % (x, y, z))

        axislist = ['1 0 0 1','0 1 0 1','0 0 1 1']
        negaxislist = ['-1 0 0 1','0 -1 0 1','0 0 -1 1']
        for normal_num in range(0,var_count,3):
            normal_list=[]
            for i in range(3):
                normal_list.append([])
                for var in [X, Y, Z]:
                    normal_list[i].append(var_list[normal_num+i][var])
            response = self.evalutate(self.get_normal(normal_list))
            if response == "x":
                uaxis = axislist[1]
            else:
                uaxis = axislist[0]
            if response == "z":
                vaxis = negaxislist[1]
            else:
                vaxis = negaxislist[2]
            vmf_template = vmf_template.replace('AXIS_REPLACE_U',uaxis,1)
            vmf_template = vmf_template.replace('AXIS_REPLACE_V',vaxis,1)
        
    def evaluate(self, coords):
        dist_x,dist_y,dist_z = abs(coords[0]),abs(coords[1]),abs(coords[2]) 
        if dist_x >= dist_y and dist_x >= dist_z:
            return "x"
        elif dist_y >= dist_z:
            return "y"
        return "z"

    def get_normal(self, coord_list):
        vector_a = (coord_list[1][0]-coord_list[0][0],coord_list[1][1]-coord_list[0][1],coord_list[1][2]-coord_list[0][2])
        vector_b = (coord_list[2][0]-coord_list[0][0],coord_list[2][1]-coord_list[0][1],coord_list[2][2]-coord_list[0][2])
        
        normal = (vector_a[1]*vector_b[2]-vector_a[2]*vector_b[1],vector_a[2]*vector_b[0]-vector_a[0]*vector_b[2],vector_a[0]*vector_b[1]-vector_a[1]*vector_b[0])
        return normal

    def rotatePoint(self, centerPoint,point,angle):
        angle = math.radians(angle)
        temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
        temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
        return temp_point
