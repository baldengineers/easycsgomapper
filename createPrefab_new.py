"""
Every prefab file should include 
* Algorithm to construct prefab (current method needs to be changed entirely)
* a set of points, with the origin in the top-left corner, defining the vertices of the icon. This will help the grid widget draw the icon
* something to calculate the colors in the icon - e.g. list of pixels, jpg image. list of pixels may save space
"""

import re
import sys
import itertools
import math
import numpy as np
import subprocess
import geo
from GridWidget import CreatePrefabGridWidget
from cpp_exe.vmfScript import *
from PySide.QtCore import *
from PySide.QtGui import *

class Create():
    def __init__(self, show=True):
        if show:
            self.dialog = QDialog()

            self.buggyText = QLabel("This is a pretty buggy tool at this point, and is mostly used by developers. Are you sure you want to do this? \n(exported prefabs can be found in the main directory, where the executable is.)")
            self.textLineEdit = QLineEdit()
            self.nameLineEdit = QLineEdit()
            
            self.vmfLineEdit = QLineEdit()
            self.vmfLineEdit.textChanged.connect(lambda: self.icon_grid.update_draw_list(self.create_prefab(self.vmfLineEdit.text())))
            self.vmfBrowse = QPushButton("Browse",self.dialog)
            self.vmfBrowse.clicked.connect(lambda: self.vmfLineEdit.setText(QFileDialog.getOpenFileName(self.dialog, "Choose .vmf File", "/","*.vmf")[0]))
            self.vmfLayout = QHBoxLayout()
            self.vmfLayout.addWidget(self.vmfLineEdit)
            self.vmfLayout.addWidget(self.vmfBrowse)
            
            self.iconLineEdit = QLineEdit()
            self.iconBrowse = QPushButton("Browse",self.dialog)
            self.iconBrowse.clicked.connect(lambda: self.iconLineEdit.setText(QFileDialog.getOpenFileName(self.dialog, "Choose .jpg File", "/","*.jpg")[0]))
            self.iconLayout = QHBoxLayout()
            self.iconLayout.addWidget(self.iconLineEdit)
            self.iconLayout.addWidget(self.iconBrowse)

            self.expCheckBox = QCheckBox(self.dialog)
            self.sectionSelect = QComboBox()
            #needs to have a cs:go version
            #if self.isTF:
            self.sectionSelect.addItems(["Geometry","Map Layout","Fun/Other"])
            #else:
            #    pass

            self.radioLayout = QHBoxLayout()
            self.radioTF2 = QRadioButton("TF2",self.dialog)
            self.radioTF2.setChecked(True)
            self.radioCSGO = QRadioButton("CS:GO",self.dialog)
            self.group = QButtonGroup()
            self.group.addButton(self.radioTF2)
            self.group.addButton(self.radioCSGO)
            self.group.setExclusive(True)
            self.radioLayout.addWidget(self.radioTF2)
            self.radioLayout.addWidget(self.radioCSGO)

            self.icon_grid = CreatePrefabGridWidget()

            self.okay_btn = QPushButton("Create Prefab", self.dialog)
            self.okay_btn.clicked.connect(self.dialog.accept)
            self.preview_btn = QPushButton("Preview", self.dialog)
            self.preview_btn.clicked.connect(self.preview)
            self.cancel_btn = QPushButton("Cancel", self.dialog)
            self.cancel_btn.clicked.connect(self.dialog.reject)
            self.btn_layout = QHBoxLayout()
            self.btn_layout.addStretch(1)
            self.btn_layout.addWidget(self.okay_btn)
            self.btn_layout.addWidget(self.preview_btn)
            self.btn_layout.addWidget(self.cancel_btn)
            

            #self.blankstring = QWidget()
            
            self.form = QFormLayout()
            self.form.addRow(self.buggyText)
            self.form.addRow("Prefab Text:", self.textLineEdit)
            self.form.addRow("Prefab Name:", self.nameLineEdit)
            self.form.addRow("VMF file (.vmf):", self.vmfLayout)
            self.form.addRow("Icon (.jpg):", self.iconLayout)
            self.form.addRow("Export prefab?", self.expCheckBox)
            self.form.addRow("Which section?",self.sectionSelect)
            self.form.addRow("Which game?", self.radioLayout)
            self.form.addRow("icon", self.icon_grid)
##            for i in range(5):
##                self.form.addRow(self.blankstring)
            self.form.addRow(self.btn_layout)

            self.dialog.accepted.connect(lambda: self.create_prefab(self.vmfLineEdit.text(), self.nameLineEdit.text(), self.textLineEdit.text(), self.iconLineEdit.text(), self.expCheckBox.isChecked(), self.radioTF2.isChecked()))
            
            #self.dialog.setGeometry(150,150,400,300)
            self.dialog.setWindowTitle("Create Prefab")
            self.dialog.setWindowIcon(QIcon("icons\icon.ico"))

            self.dialog.setLayout(self.form)
            self.dialog.exec_()

    def preview(self):
        loadVMF(self.vmfLineEdit.text())
        self.process = subprocess.Popen('cpp_exe/viewer.exe')
#        window = QWidget()
#        window.fromWinId(process.pid)
#        window.setFlags(Qt.FramelessWindowHint)
#        container = QWidget.createWindowContainer(window)
#        layout = QVBoxLayout()
#        layout.addWidget(container)
#        self.form.addRow(layout)

    def create_prefab(self, vmf_file, prefab_name='', prefab_text='', prefab_icon='', workshop_export='', is_tf2=''):
		try:
			os.kill(self.process.pid, signal.SIGKILL)
		except:
			pass
			#i know try/excepts arent good but you gotta do it here
        #begin creating prefab
        #vmf_file | string | contains the filepath of the vmf file of the prefab
        #prefab_name | string | is the filename of the prefab file being created
        #prefab_text | string | is the name of the prefab as it will appear in the main application window
        #prefab_icon | string | is the filepath of the icon of the prefab as it will appear in the main application window
        #workshop_export | boolean | that determines whether the prefab will be zipped for export to the workshop
        self.ent_name_list = [] #list containing all targetnames
        self.var_list = [] #self.var_list contains all the variables needed to be written to the prefab.py file
        self.draw_list = [] #self.draw_list contains the points of the planes to draw when placing tile on gridWidget
        self.c_dict = {} #self.c_dict (coordinate dict.) is a dictionary of the x, y, and z's so you can reference them later. ex: {x1 : 512, y1 : -512, z1: 192}
        self.var_num = 0 #self.var_num is the number that appears after the variable. ex. (x1 y1 z1) (x2 y2 z2) (x3 y3 z3)
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
            tlist = "".join(tlist).split()
            
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
        block_type = "" #block_type contains the current block of code the program is currently looking at. A block of code is determined by the two brackets {}/()/[] surrounding it.
        block_dict = {}
        key = ""
        value = ""
        
        with open(vmf_file, "r") as f:
            self.vmf_data = f.readlines()
            header = True #header is used to get rid of the header at the beginning of the vmf file

            for index, line in enumerate(self.vmf_data):
                key = ""
                value = ""
                if "\"" in line:
                    line_sep = self.separate("Q",line) #line separated by the quotes as a tuple
                    key = line_sep[0]
                    value = line_sep[1]
                    #for example, in "lightmapscale" "16", lightmapscale is the key, 16 is the value
                elif "{" not in line and "}" not in line:
                    block_type = line.strip() #isolates the title of code blocks such as "solid" or "side"
                else: #need to use key and block_title vars because a model/texture name might have the words in them. e.g. a texture called "farside", it has "side" in it
                    if "{" in line:
                        block_dict[line.count("\t")] = block_type
                    elif "}" in line:
                        end = block_dict[line.count("\t")] #detects which block is "ending"
                        if end == "solid":
                            X,Y,Z = 0,1,2
                            cur_p_vals = np.absolute(cur_p_vals).tolist()
                            points = list(k for k,_ in itertools.groupby(sorted([item for sublist in cur_p_vals for item in sublist]))) #removes duplicate points
                            for p in points:
                                for i, pl in enumerate(cur_p_vals):
                                    if geo.coplanar(pl,p):
                                        #print("cop")
                                        cur_p_vals[i] += [p]
                            a = [geo.area(pl) for pl in cur_p_vals]
                            self.draw_list.append(cur_p_vals[a.index(max(a))])
                            self.draw_list[-1] = geo.sortPtsClockwise(self.draw_list[-1])
                    continue
                
                #structure for the below if statement:
                #1: if key == ...
                #2: elif block_type == ...

                if key == "id":
                    if block_type == "solid" or block_type == "entity":
                        id_var = "world_id_num"
                    elif block_type == "side":
                        id_var = "id_num"
                    else:
                        continue
                    self.vmf_data[index] = self.vmf_data[index].replace(value, id_var)
                    
                    
                elif block_type == "solid":
                    if header:
                        header = False
                        for i in range(index):
                            self.vmf_data[i] = ""
                    cur_p_vals = [] #resets the list used for determining the current points in the current solid
                elif block_type == "side":
                    if key == "plane":
                        p_vals = list(self.separate("P",value)) #contains all 3 point values of the plane
                        """
                        The following block assigns the variable if it has not been assigned already,
                        and converts the coordinates into integers ("512 -512 192" becomes [512,-512,192]
                        and "x1 y1 z1" is converted into its already assigned integer values)
                        """
                        for i, p_val in enumerate(p_vals): 
                            if not "x" in p_val:
                                p_vals[i] = [int(float(p)) for p in p_val.split()]
                                self.assign_var(p_vals[i], index)
                            else:
                                var_num = int(p_val.split()[0][1:])
                                p_vals[i] = [self.c_dict["%s%d" % (var, var_num)] for var in ["x", "y", "z"]]
                        cur_p_vals.append(p_vals)
                    elif key == "uaxis" or key == "vaxis":
                        replace = self.separate("B", value, "\[", "\]")[0]
                        self.vmf_data[index] = self.vmf_data[index].replace(replace, "AXIS_REPLACE_%s" %("U" if key == "uaxis" else "V"))
                elif block_type == "entity":
                    if key == "angles":
                        anglevallist = value.split()
                        self.vmf_data[index] = self.vmf_data[index].replace(value,"#ROTATION_%s_%s_%s" % (anglevallist[0],anglevallist[1],anglevallist[2]))  
                    elif key == "origin":
                        if "x" not in value:
                            self.assign_var([int(v) for v in value.split()], index)
                    elif key == "targetname":
                        #some way for it to add the targetname to a list of targetnames that is added to a list
                        #here, and when the .py is run, it replaces all instances of the targetname with tgname_<id_num>
                        
                        #when it replaces all instances of that targetname, we don't even need to touch the connections
                        #block_type at all.
                        
                        self.ent_name_list.append(value)
                        
                        pass
                elif block_type == "cameras":
                    del self.vmf_data[index:]
                    
                
                    

##        print("vmf_data: ")
##        for i in self.vmf_data:
##            print(i)
##        print("var_list: ",self.var_list)
        print("draw_list: ",self.draw_list)
        return self.draw_list

##        with open('tf2/prefabs/prefab_new.py', 'a') as f:
##            for item in self.vmf_data:
##                f.write(item)
##            for item in self.var_list:
##                f.write(item+'\n')
        
        #ent name shit
        ent_name_str="    for ent_name in ["
        for i in self.ent_name_list:
            ent_name_str+=i+"," 
        ent_name_str=ent_name_str[:-1]+"""]:
        ent_values = ent_values.replace(ent_name,"tname_%d" % entity_num)    
        """
        
        #now replace
                        
    def assign_var(self, p_val, index):
        #assigns values for the variables (x1,y1,z1,x2,etc...) and writes them to self.var_list
        #p_val is the coord values for the point

        X,Y,Z = 0,1,2 #Constants to make managing the indices of p_val[] easier
            
        self.var_list.append("xy%d = int(rotatePoint((posx*scale+scale/2,posy*-1*scale-scale/2), (posx*scale+%d, posy*-1*scale+%d), (360 if rotation!=0 else 0)-90*rotation))" % (self.var_num, p_val[X], p_val[Y]))
        for var in ["x","y"]:
            self.var_list.append("%s%d = xy%d[%s]" % (var, self.var_num, self.var_num, 0 if var == "x" else 1))
        self.var_list.append("z%d = %d" % (self.var_num, p_val[Z]))

        for index in range(index,len(self.vmf_data)):
            line_sep = self.separate("Q",self.vmf_data[index])
            key = line_sep[0] if line_sep else None
            if key and not key == "angles":
                if ' '.join([str(p) for p in p_val]) in self.vmf_data[index]:
                    self.vmf_data[index] = self.vmf_data[index].replace("(%d %d %d)" % (p_val[X], p_val[Y], p_val[Z]), "(x%d y%d z%d)" % (self.var_num, self.var_num, self.var_num)) #replaces the plane values
                    self.vmf_data[index] = self.vmf_data[index].replace("\"%d %d %d\"" % (p_val[X], p_val[Y], p_val[Z]), "\"x%d y%d z%d\"" % (self.var_num, self.var_num, self.var_num)) #replaces the entity values
                    
        self.c_dict.update({"x%d" % (self.var_num) : p_val[X], "y%d" % (self.var_num) : p_val[Y], "z%d" % (self.var_num) : p_val[Z]})
        
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
 
        return re.search(ex,s).groups() if re.search(ex,s) else None #check if NoneType

    

if __name__ == '__main__':
    #xd = Create("C:/Users/Jonathan/Documents/GitHub/mapper/dev/block.vmf", "prefab_name", "prefab_text", "prefab_icon", "workshop_export", is_tf2=True)

    #xd = Create(False)
    #xd.create_prefab("C:/Users/Jonathan/Documents/GitHub/mapper/dev/gridtest.vmf", "prefab_name", "prefab_text", "prefab_icon", "workshop_export", is_tf2=True)
    app = QApplication(sys.argv)
    main = Create()
    
