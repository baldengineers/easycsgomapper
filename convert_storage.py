import pickle
import os
all_list,cur=[[]],0
for pfb_file in ["prefab_list.txt","prefab_icon_list.txt","prefab_text_list.txt"]:
    cfile= open("tf2/prefab_template/"+pfb_file,"r")
    all_list.append(cfile.readlines())
    count = len(cfile.readlines())
    cfile.close()
for index in all_list[1]:
    if index == "\n":
        cur+=0
    else:
        all_list[3].append(cur)
for i in range(cur):
    for b in range(1,4):
        del all_list[b][all_list[b].index("\n")]

prefab = open("tf2/prefabs/pfinfo.ezmd","wb")
pickle.dump(all_list,prefab)
prefab.close()
