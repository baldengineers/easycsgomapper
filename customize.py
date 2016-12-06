import vpk
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import pickle
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
##        print("Files:")
##        for file in sorted(self.currentOtherFilesInDir[0]):
##            print("-"+file)
##        print("Dirs:")
##        for direc in sorted(self.currentOtherFilesInDir[1]):
##            print("-"+direc)
        return sorted(self.currentOtherFilesInDir[0])

def loadVMF(filepath):
    with open(filepath, "r") as f:
        vmf_tmp_lst = f.readlines()
        vmf_tmp_str = "".join(f.readlines())

    return vmf_tmp_lst, vmf_tmp_str

def loadPickledVPK():
    global mat_vpk, mod_vpk
    mat_vpk = pickle.load(open("tf2/mat_vpk.pvpk","rb"))
    mod_vpk = pickle.load(open("tf2/mod_vpk.pvpk","rb"))

def savePickledVPK():
    print("pickling vpk files as file tree...")
    with open("tf2/mat_vpk.pvpk", "wb") as mat_file:
        pickle.dump(makeFileTree(loadVPKfiles("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/tf2_textures_dir.vpk")), mat_file)
    with open("tf2/mod_vpk.pvpk", "wb") as mod_file:
        pickle.dump(makeFileTree(loadVPKfiles("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/tf2_misc_dir.vpk")),mod_file)
        

def processVMF(vmf_text):
    vmf_text_lst = vmf_text[0]
    material_list = []
    prop_list     = []
    logic_list    = []
    for line in vmf_text_lst:
        if "\" \"" in line:
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
    return material_list,prop_list,logic_list

def loadVPKfiles(filepath):
    pak = vpk.open(filepath)
    temp_list = []

    for path in pak:
        temp_list.append(path)

    return temp_list

class IDButton(QPushButton):
    def __init__(self, btn_id):
        super(IDButton,self).__init__()
        self.id = btn_id
        #very usefule butone
 
class selectPage(QWizardPage):
    def __init__(self, parent):
        super(selectPage,self).__init__(parent)
        self.setTitle("Choose customizable assets")

        self.customTabs = QTabWidget()
        #self.checkboxList = []

        #self.listLayout = [(QVBoxLayout(),"Textures"),(QVBoxLayout(),"Models"),(QVBoxLayout(),"Logic")]
        parent.listList = [(QListWidget(),"Textures"),(QListWidget(),"Models"),(QListWidget(),"Logic")]
        for i,level in enumerate(parent.all_lists):
            #parent.listList[i][0].itemClicked.connect(lambda: self.clearSecond(parent))
            for item in level:
                x = QListWidgetItem(item, parent.listList[i][0])
                x.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                x.setCheckState(Qt.Unchecked)

        for l in parent.listList:
            self.customTabs.addTab(l[0],l[1])

        self.realNextBtn = QPushButton()
        self.realNextBtn.setText("next")
        self.realNextBtn.clicked.connect(lambda: parent.setPage(parent.nextId()))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.customTabs)
        #self.layout.addWidget(self.realNextBtn)
        self.setLayout(self.layout)
        self.setButtonText(parent.NextButton, "Continue")

class editPage(QWizardPage):
    def __init__(self, parent):
        super(editPage,self).__init__(parent)
        self.setTitle("Create and edit styles")
        self.parent = parent

        self.styleCount = -1

        
        
        #default labels
        self.TYPELIST        = ["MATERIAL","MODEL","LOGIC ENTITY"]
        self.DEFAULTLIST     = ["Original material:","Original model:","Original name:"]
        self.NEWLIST         = ["Styled material:","Styled model:","New name:"]
        self.CREATENEWSTYLE  = "Create New Style"
        self.REMOVESTYLE     = "Remove Style:"
        self.STYLE           = "Style:"

        #define page layout
        self.edit_page_layout = QVBoxLayout()
        self.epl = QVBoxLayout()
        self.eplw = QWidget()

        #define lists of edit layouts
        self.editList = [[[] , []]]
        self.styleList = [[]]
        self.logicEditList    = [] #may haved to be changed due to complexity of problem

        #add style button
        self.addStyleButton = QPushButton()
        self.addStyleButton.setText(self.CREATENEWSTYLE)
        self.addStyleButton.clicked.connect(self.newStyle)

        #default material edit layout (reference
##        self.titleVBox = QVBoxLayout()
##        self.titleVBox.addWidget(self.DEFAULTMATERIAL)
##        self.titleVBox.addWidget( MATERIAL_DEFAULT_PATH.lower() )
##        self.editVBox = QVBoxLayout()
##        self.editVBox.addWidget(self.NEWMATERIAL)
##        self.editVBox.addWidget(QLineEdit containing material's default material by default)
##        self.additionalVBox = QVBoxLayout()
##        self.additionalVBox.addWidget(QButton that puts a dropdown containing other files in dir of mat)
##        self.additionalVBox.addWidget(QButton that puts a lineedit that works as a query through the mat vpk)
##        self.additionalVBox.addWidget(QButton that pops up a file browser that represents the vpk)
##        self.totalLayout = QHBoxLayout()
##        self.totalLayout.addLayout(self.titleVBox)
##        self.totalLayout.addLayout(self.editVBox)
##        self.totalLayout.addLayout(self.additionalVBox)
    def initializePage(self):
        self.edit_page_layout = QVBoxLayout()
        self.checkChecked(self.parent)
        
        style = QHBoxLayout()
        style.addWidget(QLabel(self.STYLE))
        self.originalStyle = QLineEdit("Default")
        style.addWidget(self.originalStyle)
        self.styleList[self.styleCount].append(style)
        for ind, section in enumerate(self.acceptedList):
            for i,item in enumerate(section):
                #print(i)
                self.styleList[self.styleCount].append(self.createEdit(self.parent, item,ind,i,False, self.styleCount))
        
        self.scrollarea = QScrollArea()
        for i,x in enumerate(self.styleList):
            if i != 0:
                div = QFrame()
                div.setFrameStyle(QFrame.HLine)
                div.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
                self.epl.addWidget(div)
            for z in x:
                self.epl.addLayout(z)

        self.eplw.setLayout(self.epl)
        self.scrollarea.setWidget(self.eplw)
        self.edit_page_layout.addWidget(self.scrollarea)
        self.edit_page_layout.addWidget(self.addStyleButton)
        #selectPagef.edit_page_layout.addWidget(QLabel("tst"))

        self.setLayout(self.edit_page_layout)
        self.styleCount += 1

    def newStyle(self):
        for ind, section in enumerate(self.acceptedList):
            for i,item in enumerate(section):
                #print(i)
                self.styleList[self.styleCount].append(self.createEdit(self.parent, item,ind,i,True, self.styleCount))       

    def createEdit(self, parent, name, mtype, place, default, style):
        #parent is the qwizard class
        #name is the path of the material or model. will be something else for logic
        #mtype is the type of item it is (0 = material, 1 = model, 2 = logic)
        #place is the index of the item in its category
        #default is whether or not it's created on page init/part of default style
        #style is the integer representing the index of hte style it belongs to
        if mtype != 2:
            tVBox = QHBoxLayout()
            tVBox.addWidget(QLabel(self.DEFAULTLIST[mtype]))
            tVBox.addWidget(QLabel(name))
            eVBox = QHBoxLayout()
            eVBox.addWidget(QLabel(self.NEWLIST[mtype]))
            if not default:
                #change to disabled when done with testing
                newEdit = QLineEdit(name)
                newEdit.setReadOnly(True)
                if mtype == 0:
                    ddButton = IDButton(self.parent.cur_id_mat)
                    parent.cur_id_mat += 1
                else:
                    ddButton = IDButton(self.parent.cur_id_mod)
                    parent.cur_id_mod += 1
                ddButton.setEnabled(False)
            else:
                newEdit = QLineEdit(name).setEnabled(True)
                ddButton = IDButton(parent.cur_id).setEnabled(True)
            self.editList[style][mtype].append(newEdit)
            eVBox.addWidget(newEdit)
            aVBox = QHBoxLayout()
            if mtype == 0:
                ddButton.setText("Change Texture")
                ddButton.clicked.connect(lambda: self.makeDD("materials/"+str(self.editList[style][mtype][place].text()).lower()+".vtf", ddButton.id, mtype, self.styleCount))
            else:
                ddButton.setText("Change Model")
                ddButton.clicked.connect(lambda: self.makeDD(str(self.editList[style][mtype][place].text()).lower(), ddButton.id, mtype, self.styleCount))
            aVBox.addWidget(ddButton)
            #include other methods of easing access later

            allLayout = QVBoxLayout()
            allLayout.addWidget(QLabel(self.TYPELIST[mtype]))
            allLayout.addLayout(tVBox)
            allLayout.addLayout(eVBox)
            allLayout.addLayout(aVBox)
            allLayout.setAlignment(Qt.AlignRight)
            allLayout2 = QHBoxLayout()
            allLayout2.addSpacing(20)
            allLayout2.addLayout(allLayout)
            #allLayout.setMaximumSize(QSize(200,100))

            
            return allLayout2 
            
    def makeDD(self,filedir,itemid, mt, style):
        print(filedir) 
        if mt == 0:
            filelist = mat_vpk.getOtherFilesInDirectory(filedir)
            head = "/".join(filedir.split("/")[0:len(filedir.split("/"))-1]).replace("materials/","").upper()+"/"
        elif mt == 1:
            filelist = mod_vpk.getOtherFilesInDirectory(filedir)
            head = "/".join(filedir.split("/")[0:len(filedir.split("/"))-1])+"/"
        #print(filelist)
        #temporary
        popup = QDialog(self)
        popup.setGeometry(100,100,290,350)
        mainLO = QHBoxLayout()


        filelistwid = QListWidget()
        for file in filelist:
            if ".mdl" in file or ".vtf" in file:
                filelistwid.addItem(file)
        mainLO.addWidget(filelistwid)
        
        if mt == 0:
            filelistwid.itemClicked.connect(lambda: self.editList[style][mt][itemid].setText(head+str(filelistwid.currentItem().text()).replace(".vtf","").upper()))
        if mt == 1:
            filelistwid.itemClicked.connect(lambda: self.editList[style][mt][itemid].setText(head+str(filelistwid.currentItem().text())))               
                            
        popup.setLayout(mainLO)
        popup.setWindowTitle("Choose file")
        popup.exec_()

    def checkChecked(self, parent):
        self.acceptedList = [ [] , [] , [] ]
        for i in range(3):
            for item_ind in range(parent.listList[i][0].count()):
                if parent.listList[i][0].item(item_ind).checkState() == Qt.Checked:
                    self.acceptedList[i].append(parent.listList[i][0].item(item_ind).text().replace("\n",""))
        print(self.acceptedList)



        
class customizeWizard(QWizard):
    def __init__(self,vmf_path):
        super(customizeWizard,self).__init__()

        self.all_lists = processVMF(loadVMF(vmf_path))
        self.cur_id_mat,self.cur_id_mod = 0,0

        self.addPage(selectPage(self))
        self.addPage(editPage(self))
        self.show()


##lists = processVMF(loadVMF())
loadPickledVPK()
app = QApplication(sys.argv)
f = customizeWizard("dev/shtie.vmf")
sys.exit(app.exec_())
