import vpk
#for getting all texture filenames/paths

class makeFileTree():
    def __init__(self,path_list):
        self.path_list = path_list
        self.slashct = 0

        #determine largest # of directories
        for path in path_list:
            if path.count("/") > self.slashct:
                self.slashct = path.count("/")
                
        #organisation:
        #main dir is list containing number of subdirs
        # eg. if there's a system like ./a/ and ./b/
        #                  ./a/1/ and ./a/2/     ./b/1 and ./b/2/
        # [ [#a [#1], [#2]], [#b [#1], [#2]] ]
        #each "dir" or list can contain lists (subdirs) or strings (paths)

        
    

def loadVMF(filepath):
    with open(filepath, "r") as f:
        vmf_tmp_lst = f.readlines()
        vmf_tmp_str = "".join(f.readlines())

def processVMF(vmf_text_str,vmf_text_lst):
    material_list = []
    prop_list     = []
    logic_list    = []
    for line in vmf_text_lst:
        info = line.split("\" \"")[1].replace("\"","")
        if "\"material\"" in line:
            material_list.append(info) #appends texture to list of all textures in vmf
        elif "\"model\"" in line:
            prop_list.append(info) #appends model to list of all models in vmf
        elif "\"targetname\"" in line:
            logic_list.append(info) #appends name of entity to list of all entities in vmf
        #this code should be for changing names of entities for
        #game logic (eg. triggers + receptors) based off
        #team color, style, or prefab option

    #remove dupes, not possible with loops
    material_list = list(set(material_list))
    prop_list     = list(set(prop_list))
    logic_list    = list(set(logic_list))

def loadVPKfiles(filepath):
    pak = vpk.open(filepath)
    temp_list = []

    for path in pak:
        temp_list.append(path)

    return temp_list
