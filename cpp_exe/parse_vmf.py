#.vmf parser (basic)



def loadVMF(filename):
    sidelist = []
    vertlist = []
    with open(filename, 'r') as f:
        vmfDataList = f.readlines()
    for index, line in enumerate(vmfDataList):
        line = line.strip()
        if "plane" in line:
            string = line.split('\" \"')[1].replace('"','').replace("(", " ").replace(")", " ")
            vertlist.append(string[1:-1].split("   "))
    for index,side in enumerate(vertlist):
        sidelist.append([])
        for i in range(3):
            sidelist[index].append([])
            sidelist[index][i] = side[i].split(' ')
    #print(sidelist)
    return sidelist

loadVMF("test.vmf")




##            cleanline = line.strip()
##            if cleanline == "{":
##                self.layer += 1
##                self.all_dict[self.vmfDataList[index-1]] =
##            else if cleanline == "}":
##                self.layer -= 1
            
