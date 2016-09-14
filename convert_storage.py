import pickle
import os
all_list = [[]]
cur = 0 #current tab
dlist =[] #for indices of other lists that need to be deleted
for pfb_file in ["prefab_list.txt","prefab_icon_list.txt","prefab_text_list.txt"]:
    with open("tf2/prefab_template/"+pfb_file,"r") as cfile:
        all_list.append(cfile.read().splitlines())
for ind,item in enumerate(all_list[1]):
    if item == "":
        print(ind)
        cur+=1
        dlist.append(ind)
    else:
        all_list[0].append(cur) #appends the tab that the prefab is in

for index,i in enumerate(all_list):
    if index != 0:
        for sind,p in enumerate(dlist):
            del i[p-sind]
        
with open("tf2/prefabs/pfinfo.ezmd","wb") as f:
    pickle.dump(all_list,f)

l = pickle.load(open("tf2/prefabs/pfinfo.ezmd","rb"))
#print(line for line in l)
