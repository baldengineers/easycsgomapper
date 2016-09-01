class Create():
    def __init__(self, vmf_file, prefab_name, prefab_text, prefab_icon, workshop_export, is_tf2):
        #vmf_file | string | contains the filepath of the vmf file of the prefab
        #prefab_name | string | is the filename of the prefab file being created
        #prefab_text | string | is the name of the prefab as it will appear in the main application window
        #prefab_icon | string | is the filepath of the icon of the prefab as it will appear in the main application window
        #workshop_export | boolean | that determines whether the prefab will be zipped for export to the workshop
        #indexLine |  | I have no fucking idea
        #index |  | I have no idea about this either

        self.LEVEL_HEIGHT = 448 #self.LEVEL_HEIGHT is the constant for the height of each level of the map.
        self.var_list = [] #self.var_list contains all the variables needed to be written to the prefab.py file
        self.var_num = 1 #self.var_num is the number that appears after the variable. ex. (x1 y1 z1) (x2 y2 z2) (x3 y3 z3)
        self.compile_list = [ #self.compilelist is the outline of the prefab.py file
        """import os
import math
def rotatePoint(centerPoint,point,angle):
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point
def createTile(posx, posy, id_num, world_id_num, entity_num, placeholder_list, rotation, level):

    looplist = '1'
    values=[]#Values are all of the lines of a prefab that have the vertex coords
""",

  "#INSERT_OPEN_FILE\n",

  """
    lines = f.readlines() #gathers each line of the prefab and puts numbers them
""",

  "#INSERT_PY_LIST\n",

  "#INSERT_VAR_COUNT\n",

  """
    values = "".join(lines)#converting list to string
    ogvalues = "".join(lines)
    normal_list,axislist,negaxislist,vaxis,uaxis=[],['1 0 0 1','0 1 0 1','0 0 1 1'],['-1 0 0 1','0 -1 0 1','0 0 -1 1'],0,0
    def evaluate(coords):
        dist_x,dist_y,dist_z = abs(coords[0]),abs(coords[1]),abs(coords[2]),
        if dist_x >= dist_y and dist_x >= dist_z:
            return axislist[0]
        if dist_y >= dist_z:
            return axislist[1]
        return axislist[2]
    def get_normal(coord_list):
        vector_a = (coord_list[1][0]-coord_list[0][0],coord_list[1][1]-coord_list[0][1],coord_list[1][2]-coord_list[0][2])
        vector_b = (coord_list[2][0]-coord_list[0][0],coord_list[2][1]-coord_list[0][1],coord_list[2][2]-coord_list[0][2])

        normal = (vector_a[1]*vector_b[2]-vector_a[2]*vector_b[1],vector_a[2]*vector_b[0]-vector_a[0]*vector_b[2],vector_a[0]*vector_b[1]-vector_a[1]*vector_b[0])
        return normal

    for normal_num in range(1,var_count+1,3):
        normal_list=[]
        for i in range(3):
            normal_list.append([])
            for var in ["x", "y", "z"]:
                normal_list[i].append(eval(var+str(normal_num+i)))
        coords = get_normal(normal_list)
        response = evaluate(coords)
        if response == axislist[0]:
            uaxis = axislist[1]
        else:
            uaxis = axislist[0]
        if response == axislist[2]:
            vaxis = negaxislist[1]
        else:
            vaxis = negaxislist[2]
        values = values.replace('AXIS_REPLACE_U',uaxis,1)
        values = values.replace('AXIS_REPLACE_V',vaxis,1)

    for i in range(ogvalues.count("world_idnum")):
        values = values.replace('world_idnum', str(world_id_num), 1)
        world_id_num += 1

    for var in ["x", "y", "z"]:
        for count in range(1,var_count+1):
            string = var + str(count)
            string_var = str(eval(var + str(count)))
            if var == "z":
                values = values.replace(string + ")",string_var + ")") #we need to do this or else it will mess up on 2 digit numbers
            else:
                values = values.replace(string + " ",string_var + " ")
    for i in range(ogvalues.count('id_num')):
        values = values.replace('id_num', str(id_num), 1)
        id_num = id_num+1
        """,

        "#INSERT_ENT_CODE\n",]

#here is entity code, feel free to change. only added to get the new entity rotation code in.        
  ent_code =["#INSERT_ENT_OPEN_FILE\n",

             """
    lines_ent = g.readlines()
    rot_replace_list=[]
    for index,line in enumerate(lines_ent):
        if "#ROTATION_" in line:
            us_count = 0
            tlist=[]
            for char in line:
                if us_count == 1:
                    tlist.append(char)
                if char == "_":
                    us_count += 1
            old = "".join(tlist)
            tlist = "".join(tlist).split(' ')
            
            rot_replace_list.append([line,"%s" % str(int(tlist[0])*(-90))+' '+str(int(tlist[1])*(-90))+' '+str(int(tlist[2])*(-90)),index])
    for rep in rot_replace_list:
        lines_ent[rep[2]] = lines_ent[rep[2]].replace('#ROTATION_'+rep[0],rep[1])
""",

             "#INSERT_ROT_IF\n",

             "#INSERT_ENT_PY_LIST\n",

             "#INSERT_ROT_ENT_CODE\n",
             
             "#INSERT_ENT_VAR_COUNT\n",

"""
    ent_values = "".join(lines_ent)
    ent_values_split = ent_values.split("\\"")
    valcount = "".join(lines_ent)

    for item in ent_values_split:
        if "entity_name" in item or "parent_name" in item or "door_large" in item:
            placeholder_list.append(item)

    for i in range(valcount.count('world_idnum')):
        ent_values = ent_values.replace('world_idnum', str(world_id_num), 1)
        world_id_num += 1

    for var in ["px", "py", "pz"]:
        for count in range(1,ent_var_count+1):
            string = var + str(count)
            string_var = str(eval(var + str(count)))

            if var == "pz":
                ent_values = ent_values.replace(string + "\\"",string_var + "\\"") #we need to do this or else it will mess up on 2 digit numbers
            else:
                ent_values = ent_values.replace(string + " ",string_var + " ")
                
    for var in ["x", "y", "z"]:
        for count in range(1,var_count+1):
            try:
                string = var + str(count)
                string_var = str(eval(var + str(count)))
                if var == "z":
                    ent_values = ent_values.replace(string + ")",string_var + ")") #we need to do this or else it will mess up on 2 digit numbers
                else:
                    ent_values = ent_values.replace(string + " ",string_var + " ")
            except:
                pass

    for i in range(valcount.count('id_num')):
        ent_values = ent_values.replace('id_num', str(id_num), 1)
        id_num = id_num+1

    for i in range(int(valcount.count('laser_target')/2)):
        if "laser_target_plac" in ent_values:
            ent_values = ent_values.replace("laser_target_plac", "laser_target" + str(entity_num), 2)
            entity_num += 1

    for i in range(int(valcount.count('sound'))):
        if "sound_plac" in ent_values:
            ent_values = ent_values.replace("sound_plac", "AmbSound"+str(entity_num), 2)
            ent_values = ent_values.replace("relay_plac", "LogicRelay"+str(entity_num),2)
            entity_num += 1

    for i in range(valcount.count("entity_name")):
        try:
            ent_values = ent_values.replace("entity_name", "entity" + str(entity_num), 1)
            ent_values = ent_values.replace("entity_same", "entity" + str(entity_num), 1)
            if "parent_name" in placeholder_list[entity_num]:
                ent_values = ent_values.replace("parent_name", "entity" + str(entity_num), 1)
                placeholder_list.remove(placeholder_list[entity_num])
            
            if "door_large" in ent_values:
                ent_values = ent_values.replace("door_large", "door_large" + str(entity_num), 4)
            if "\\"respawn_name\\"" in ent_values:
                ent_values = ent_values.replace("\\"respawn_name\\"", "\\"respawn_name" + str(entity_num) + "\\"", 2)
            entity_num += 1
        except Exception as e:
            print(str(e))

    for i in range(valcount.count("#ROTATION_")):
        ent_values = ent_values.replace

        entity_num += 1
"""]
        block_type = "" #block_type contains the current block of code the program is currently looking at. A block of code is determined by the two brackets {}/()/[] surrounding it.
        
        with open(vmf_file, "r") as f:
            vmf_data = f.readlines()
            header = True #header is used to get rid of the header at the beginning of the vmf file

            for index, line in enumerate(vmf_data):
                if "\"" in line:
                    key = self.between(line, "\"", "\"")
                    #for example, in "lightmapscale" "16", lightmapscale is the key
                elif "{" not in line and "}" not in line:
                    block_title = line.replace(" ","") #isolates the title of code blocks such as "solid" or "side"
                else: #need to use key and block_title vars because a model/texture name might have the words in them. e.g. a texture called "farside", it has "side" in it
                    continue
                
                #structure for the below if statement:
                #1: if block_title == ...
                #2: if block_type == ...
                #3: if key == ...
                    
                if block_title == "solid":
                    if header:
                        header = False
                        vmf_data[:index] = ""
                    block_type = "solid"
                elif block_title == "side":
                    block_type = "side"
                elif block_title == "entity":
                    block_type = "entity"
                elif block_type == "side":
                    if key == "plane":
                        for char_index, char in enumerate(line):
                            if char == "(":
                                num = ["","",""] #num is for the numbers in the parenthesis that are the points for the plane, it is a list of STRINGS
                                num_index = 0 #current index for the num variable above
                                if "X" not in self.between(line,f_ind=char_index,last=")"):
                                    block_type = "()"
                                else:
                                    pass
                            elif block_type == "()":
                                if not char == " ":
                                    if not char == ")":
                                        num[num_index] += char
                                    else:
                                        self.assign_var(num, line)
                                        block_type = "side"
                                else:
                                    num_index += 1
                    elif key == "uaxis" or key == "vaxis":
                        replace = self.between(line, "[", "]")
                        line.replace(replace, "AXIS_REPLACE_%s" %("U" if key == "uaxis" else "V"))
                elif block_type == "entity":
                    if key == "":
                elif key == "id":
                    if block_type == "solid" or block_type == "entity":
                        id_var = "world_idnum"
                    elif block_type == "side":
                        id_var = "id_num"
                    vmf_data[index] = between(line,"\"","\"",i=3)
                    vmf_data[index] = vmf_data[:vmf_data[index].index("id")+5] + id_var + "\"" #This line does this: "id" " + id_var + "
                        
    def assign_var(self, num, line):
        #assigns values for the variables (x1,y1,z1,x2,etc...) and writes them to self.var_list
        X,Y,Z = 0,1,2 #Constants to make managing the indices of num[] easier
            
        self.var_list.append("xy%d = int(rotatePoint((posx*512+256,posy*-1*512-256), (posx*512%s, posy*-512%s), (360 if rotation!=0 else 0)-90*rotation))" %(var_num, ("+" + num[X]) if num[X] != 0 else "", ("+" + num[Y]) if num[Y] != 0 else ""))
        for var in ["x","y"]:
            self.var_list.append("%s%d = xy%d[%s]" %(var, self.var_num, self.var_num, 0 if var == "x" else 1))
        self.var_list.append("z%d = level*%d + %d" %(self.var_num, LEVEL_HEIGHT, num[Z]))
        
        vmf_data.replace("(" + self.between(line,"(",")") + ")", "(x%d, y%d, z%d)" %(self.var_num, self.var_num, self.var_num))
        self.var_num += 1
        
    def between(self, string="", first="", last="", f_ind=0, l_ind=0, rev=False):
        #finds a substring between the given strings
        
        #string is the string you are searching within
        #first is the first character that limits the resulting word
        #last is the last ''
        #f_ind is the index of the first character ''
        #l_ind is the index of the last character ''
        #rev is if going through string in reverse
        """
        if first or last or f_ind or l_ind:
            start = (string[string.index(last)+1:].index(first)) if first else f_ind + (len(first)) if first else 1
            end = (string.index(last, start)) if last else l_ind
            return string[start:end] 
        else:
            return ""
            """
        
        word = ""
        first_met = False
        
        if first or last or f_ind or l_ind:
            for char in string if not rev else reversed(string):
                if char == first:
                    first_met = True
                elif first_met:
                    if not char == last:
                        word+=char
                    else:
                        return word
                        #implement f_ind and l_ind
        else:
            return ""
