import re

class Create():
    def __init__(self, vmf_file, prefab_name, prefab_text, prefab_icon, workshop_export, is_tf2):
        #vmf_file | string | contains the filepath of the vmf file of the prefab
        #prefab_name | string | is the filename of the prefab file being created
        #prefab_text | string | is the name of the prefab as it will appear in the main application window
        #prefab_icon | string | is the filepath of the icon of the prefab as it will appear in the main application window
        #workshop_export | boolean | that determines whether the prefab will be zipped for export to the workshop
        #indexLine |  | I have no fucking idea
        #index |  | I have no idea about this either
        self.ent_name_list = [] #list containing all targetnames
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
            tlist = "".join(tlist).split(' ')
            
            lines_ent[index] = ([line.replace(line.split("\" \"")[1].replace("\"",""),str(int(tlist[0]*(-90))+' '+str(int(tlist[1]*(-90))+' '+str(int(tlist[2]*(-90))
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
    
    """,
   
    
    "#INSERT_ENT_NAME_CODE\n",
    
    
    """

    
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
        block_title = ""
        block_type = "" #block_type contains the current block of code the program is currently looking at. A block of code is determined by the two brackets {}/()/[] surrounding it.
        key = ""
        value = ""
        
        with open(vmf_file, "r") as f:
            self.vmf_data = f.readlines()
            header = True #header is used to get rid of the header at the beginning of the vmf file

            for index, line in enumerate(self.vmf_data):
                key = ""
                value = ""
                block_title = "" #note: don't reset block_type because that carries lasts until the bracket
                if "\"" in line:
                    line_sep = self.separate("Q",line) #line separated by the quotes as a tuple
                    key = line_sep[0]
                    value = line_sep[1]
                    #for example, in "lightmapscale" "16", lightmapscale is the key, 16 is the value
                elif "{" not in line and "}" not in line:
                    block_title = line.strip() #isolates the title of code blocks such as "solid" or "side"
                else: #need to use key and block_title vars because a model/texture name might have the words in them. e.g. a texture called "farside", it has "side" in it
                    #block_type = ""
                    continue
                
                #structure for the below if statement:
                #1: if key == ...
                #2: elif block_title == ...
                #3: elif block_type == ...

                if key == "id":
                    if block_type == "solid" or block_type == "entity":
                        id_var = "world_idnum"
                    elif block_type == "side":
                        id_var = "id_num"
                    else:
                        continue
                    self.vmf_data[index] = self.vmf_data[index].replace(value, id_var)
                elif block_title == "solid":
                    if header:
                        header = False
                        for i in range(index):
                            self.vmf_data[i] = ""
                    block_type = "solid"
                elif block_title == "side":
                    block_type = "side"
                elif block_title == "entity":
                    block_type = "entity"
                elif block_title == "cameras":
                    del self.vmf_data[index:]
                elif block_type == "side":
                    if key == "plane":
                        curr_p = 0 #current point that program is iterating through, increases at every "("
                        for char_index, char in enumerate(line):
                            if char == "(":
                                curr_p += 1
                                #num = ["","",""] #num is for the numbers in the parenthesis that are the x y z coords of the point, it is a list of STRINGS
                                num_index = 0 #current index for the num variable above
                                p_vals = self.separate("P",value) #contains all the point values of the plane in a tuple
                                if "x" not in p_vals[curr_p-1]: #must subtract 1 from curr_p to get INDEX
                                    self.assign_var(p_vals[curr_p-1])
                                else:
                                    pass
                    elif key == "uaxis" or key == "vaxis":
                        replace = self.separate("B", value, "\[", "\]")[0]
                        self.vmf_data[index] = self.vmf_data[index].replace(replace, "AXIS_REPLACE_%s" %("U" if key == "uaxis" else "V"))
                elif block_type == "entity":
                    if key == "angles":
                        anglevallist = value.split(" ")
                        self.vmf_data[index] = self.vmf_data[index].replace(value,"#ROTATION_%s_%s_%s" % (anglevallist[0],anglevallist[1],anglevallist[2]))  
                    elif key == "origin":
                        self.assign_var(value)
                    elif key == "targetname":
                        #some way for it to add the targetname to a list of targetnames that is added to a list
                        #here, and when the .py is run, it replaces all instances of the targetname with tgname_<id_num>
                        
                        #when it replaces all instances of that targetname, we don't even need to touch the connections
                        #block_type at all.
                        
                        self.ent_name_list.append(value)
                        
                        pass
                    
                
                    

        print("vmf_data: ")
        for i in self.vmf_data:
            print(i)
        print("var_list: ",self.var_list)
        
        #ent name shit
        ent_name_str="    for ent_name in ["
        ent_name_str+= i+"," for i in self.ent_name_list
        ent_name_str=ent_name_str[:-1]+"""]:
        ent_values = ent_values.replace(ent_name,"tname_%d" % entity_num)    
        """
        
        #now replace
                        
    def assign_var(self, p_val):
        #assigns values for the variables (x1,y1,z1,x2,etc...) and writes them to self.var_list
        #p_val is the coord values for the point
        
        nums = p_val.split(" ")
        X,Y,Z = 0,1,2 #Constants to make managing the indices of nums[] easier
            
        self.var_list.append("xy%d = int(rotatePoint((posx*512+256,posy*-1*512-256), (posx*512%s, posy*-512%s), (360 if rotation!=0 else 0)-90*rotation))" %(self.var_num, "+" + nums[X], "+" + nums[Y]))
        for var in ["x","y"]:
            self.var_list.append("%s%d = xy%d[%s]" %(var, self.var_num, self.var_num, 0 if var == "x" else 1))
        self.var_list.append("z%d = level*%d + %s" %(self.var_num, self.LEVEL_HEIGHT, nums[Z]))

        for index in range(len(self.vmf_data)):
            line_sep = self.separate("Q",self.vmf_data[index])
            key = line_sep[0]
            if not key == "angles":
                self.vmf_data[index] = self.vmf_data[index].replace(p_val, "x%d y%d z%d" %(self.var_num, self.var_num, self.var_num))
        self.var_num += 1
        
    def separate(self, t, s, first="", last=""):
        #separate(t) separates a string based on what you want to separate
        #t | string | is the type of line that you want to separate
        #s | string | string you want to separate
        #first and last are optional parameters to find a word between
        
        if t == "BY_QUOTE" or t == "Q":
            ex = r'"(.*?)" "(.*?)"'
        elif t == "BY_PARENTHESIS" or t == "P":
            ex = r'\((.*?)\) \((.*?)\) \((.*?)\)'
        elif t == "BETWEEN" or t == "B":
            ex = r'%s(.*?)%s' % (first, last)
        else:
            return print("%s is is not a valid separate command" % (t))

        try:    
            return re.search(ex,s).groups()
        except AttributeError: #happens if the above is NoneType
            return [""]

#xd = Create("C:/Users/Jonathan/Documents/GitHub/mapper/dev/block.vmf", "prefab_name", "prefab_text", "prefab_icon", "workshop_export", is_tf2=True)

xd = Create("C:/Users/Jonathan/Documents/GitHub/mapper/dev/ent.vmf", "prefab_name", "prefab_text", "prefab_icon", "workshop_export", is_tf2=True)
