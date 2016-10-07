def loadVMF(filename):
    vertlist = []
    fileinfo = ''
    with open(filename, 'r') as f:
        vmfDataList = f.readlines()
    for index, line in enumerate(vmfDataList):
        line = line.strip()
        if "plane" in line:
            string = line.split('\" \"')[1].replace('"','').replace("(", " ").replace(")", " ")
            vertlist.append(string[1:-1].split("   "))
    with open('vertfile.vf','w') as file:
        for i in vertlist:
            for g in i:
                fileinfo += g+"\n"
        file.write(fileinfo)   
            
    #print(sidelist)
    return sidelist


side_list = loadVMF("test.vmf")

