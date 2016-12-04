import vpk
#for getting all texture filenames/paths

class makeFileTree():
    def __init__(self,path_list):
        self.path_list = path_list
        self.dirct = 0

        self.tree = []
        self.acclist = []

        #determine largest # of directories (1 too high because last one is file?)
        for path in self.path_list:
            if path.count("/") > self.dirct:
                self.dirct = path.count("/")   
        for dirlvl in range(self.dirct):
            self.tree.append([])
            self.acclist.append([])
            for path in self.path_list:
                try:
                    current = path.split("/")[dirlvl]
                    before = '' if dirlvl == 0 else path.split("/")[dirlvl-1]
                    bf = '' if dirlvl < 2 else path.split("/")[dirlvl-2]
                    if current not in self.acclist[dirlvl]:
                        if "." in current:
                            self.acclist[dirlvl].append(current)
                            self.tree[dirlvl].append((current,before,path,dirlvl))
                    if before not in self.acclist[dirlvl-1] and dirlvl != 0:
                        self.tree[dirlvl-1].append((before,bf,"/".join(path.split("/")[0:dirlvl]),dirlvl-1))
                        self.acclist[dirlvl-1].append(before)      
                except:
                    pass
    
    def getOtherFilesInDirectory(self, path):
        #returns a tuple containing 2 tuples (1 for files, 1 for dirs)
        self.currentOtherFilesInDir = ( [],[] )
        dirf = 0
        directory = 0
        parent = ''
        #find item tuple in tree
        for dirlvl in self.tree:
            for item in dirlvl:
                if path == item[2] and not dirf:
                    parent = item[1]
                    directory = item[3]
                    dirf = 1
                    print("dir found: "+path)
        
        for item in self.tree[directory]:
            if item[1] == parent:
                #if in same dir
                if "." in item[0]:
                    #is file
                    self.currentOtherFilesInDir[0].append(item[0])
                else:
                    #is dir
                    self.currentOtherFilesInDir[1].append(item[0])
        #for testing, otherwise should just return the tuple
        print("Files:")
        for file in sorted(self.currentOtherFilesInDir[0]):
            print("-"+file)
        print("Dirs:")
        for direc in sorted(self.currentOtherFilesInDir[1]):
            print("-"+direc)

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

#for testing
if __name__ == '__main__':
    mat_vpk = makeFileTree(loadVPKfiles("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/tf2_textures_dir.vpk"))
    mat_vpk.getOtherFilesInDirectory("materials/patterns/powerhouse")

