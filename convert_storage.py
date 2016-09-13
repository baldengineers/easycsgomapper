import pickle
import os
all_list = [[]]
cur = 0 #current tab
for pfb_file in ["prefab_list.txt","prefab_icon_list.txt","prefab_text_list.txt"]:
    with open("tf2/prefab_template/"+pfb_file,"r") as cfile:
        all_list.append(cfile.read().splitlines())
for item in all_list[1]:
    if item == "\n":
        cur+=1
    else:
        all_list[3].append(cur) #appends the tab that the prefab is in

with open("tf2/prefabs/pfinfo.ezmd","wb") as f:
    pickle.dump(all_list,f)

l = pickle.load(open("tf2/prefabs/pfinfo.ezmd","rb"))
print(line for line in l)
