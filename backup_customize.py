import vpk
import sys
from PySide.QtCore import *
from PySide.QtGui import *
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

cur_id = 0

#for testing (mebbe not)
mat_vpk = makeFileTree(loadVPKfiles("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/tf2_textures_dir.vpk"))
mod_vpk = makeFileTree(loadVPKfiles("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/tf2_misc_dir.vpk"))

class IDButton(QPushButton):
    def __init__(self, btn_id):
        super(IDButton,self).__init__()
        self.id = btn_id
        #very usefule butone
 
class selectPage(QWizardPage):
    def __init__(self, parent):
        self.setTitle("Choose customizable assets")

        self.customTabs = QTabWidget()
        #self.checkboxList = []

        #self.listLayout = [(QVBoxLayout(),"Textures"),(QVBoxLayout(),"Models"),(QVBoxLayout(),"Logic")]
        parent.listList = [(QListWidget(),"Textures"),(QListWidget(),"Models"),(QListWidget(),"Logic")]
        for i,level in enumerate(parent.all_lists):
            parent.listList[i][0].itemClicked.connect(lambda: self.page_two(z=True))
            for item in level:
                x = QListWidgetItem(item, parent.listList[i][0])
                x.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                x.setCheckState(Qt.Unchecked)

        for l in self.listList:
            self.customTabs.addTab(l[0],l[1])
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.customTabs)
        self.setLayout(self.layout)
        self.setButtonText(self.NextButton, "Continue")

class editPage(QWizardPage):
    def __init__(self, parent):
        self.setTitle("Create and edit styles")
        

        #default labels
        self.TYPELIST        = [QLabel("MATERIAL"),QLabel("MODEL"),QLabel("LOGIC ENTITY")]
        self.DEFAULTLIST     = [QLabel("Original material:"),QLabel("Original model:"),QLabel("Original name:")]
        self.NEWLIST         = [QLabel("Styled material:"),QLabel("Styled model:"),QLabel("New name:")]
        self.CREATENEWSTYLE  = QLabel("Create new style:")
        self.REMOVESTYLE     = QLabel("Remove Style:")

        #define page layout
        self.edit_page_layout = QHBoxLayout()

        #define lists of edit layouts
        self.editList = [[] , []]
        self.styleList = []
        self.logicEditList    = [] #may haved to be changed due to complexity of problem

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
        self.checkChecked()

        for ind, section in enumerate(self.acceptedList):
            for i,item in enumerate(section):
                print(i)
                self.createEdit(item,ind,i,False)
        
        
        for x in self.styleList:
            self.edit_page_layout.addLayout(x)
        self.edit_page_layout.addWidget(QLabel("tst"))

        self.edit_page.setLayout(self.edit_page_layout)
       

    def createEdit(self, name, mtype, place, default):
        if mtype != 2:
            tVBox = QVBoxLayout()
            tVBox.addWidget(self.DEFAULTLIST[mtype])
            tVBox.addWidget(QLabel(name))
            eVBox = QVBoxLayout()
            eVBox.addWidget(self.NEWLIST[mtype])
            newEdit = QLineEdit()
            ddButton = IDButton(self.cur_id)
##            if not default:
##                print('1')
##                newEdit = QLineEdit().setText(name).setReadOnly(True)
##                print('2')
##                ddButton = IDButton(self.cur_id).setEnabled(False)
##            else:
##                newEdit = QLineEdit(name).setEnabled(True)
##                ddButton = IDButton(self.cur_id).setEnabled(True)
            self.cur_id += 1
            print('a')
            
            self.editList[mtype].append(newEdit)
            print('b')
            eVBox.addWidget(newEdit)
            print('c')
            aVBox = QVBoxLayout()
            print('d')
            ddButton.clicked.connect(lambda: self.makeDD(mat_vpk.getOtherFilesInDirectory("materials/"+str(self.editList[mtype][place].getText())), ddButton.id, mtype))
            print('e')
            aVBox.addWidget(ddButton)
            print('f')
            #include other methods of easing access later

            allLayout = QHBoxLayout()
            allLayout.addLayout(tVBox)
            allLayout.addLayout(eVBox)
            allLayout.addLayout(aVBox)

            
            self.styleList.append(allLayout)
            
    def makeDD(self,filelist,itemid, mt):
        #temporary
        popup = QDialog(self)
        popup.setGeometry(290,350)
        mainLO = QHBoxLayout()


        filelistwid = QListWidget()
        for file in filelist:
            filelistwid.addItem(file)
        mainLO.addWidget(filelistwid)

        filelistwid.itemClicked.connect(lambda: self.editList[mt][itemid].setText(filelistwid.currentItem()))
        popup.setLayout(mainLO)
        popup.setWindowTitle("Choose file")
        popup.exec_()
    
        
        
        
    def checkChecked(self):
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
        self.runpages()
        self.cur_id = 0
    def runpages(self):
        #all customizable
        self.intro_page = QWizardPage()
        self.intro_page.setTitle("Choose customizable assets")

        self.customTabs = QTabWidget()
        #self.checkboxList = []

        #self.listLayout = [(QVBoxLayout(),"Textures"),(QVBoxLayout(),"Models"),(QVBoxLayout(),"Logic")]
        self.listList = [(QListWidget(),"Textures"),(QListWidget(),"Models"),(QListWidget(),"Logic")]
        for i,level in enumerate(self.all_lists):
            self.listList[i][0].itemClicked.connect(lambda: self.page_two(z=True))
            for item in level:
                x = QListWidgetItem(item, self.listList[i][0])
                x.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                x.setCheckState(Qt.Unchecked)

        for l in self.listList:
            self.customTabs.addTab(l[0],l[1])
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.customTabs)
        self.intro_page.setLayout(self.layout)
        self.intro_page.setButtonText(self.NextButton, "Continue")
        self.addPage(self.intro_page)

        self.page_two()



    def page_two(self, z = False):
        #if z:
            #self.removePage(1)
            #print('all good xd')
        self.edit_page = QWizardPage()
        self.edit_page.setTitle("Create and edit styles")
        

        #default labels
        self.TYPELIST        = [QLabel("MATERIAL"),QLabel("MODEL"),QLabel("LOGIC ENTITY")]
        self.DEFAULTLIST     = [QLabel("Original material:"),QLabel("Original model:"),QLabel("Original name:")]
        self.NEWLIST         = [QLabel("Styled material:"),QLabel("Styled model:"),QLabel("New name:")]
        self.CREATENEWSTYLE  = QLabel("Create new style:")
        self.REMOVESTYLE     = QLabel("Remove Style:")

        #define page layout
        self.edit_page_layout = QHBoxLayout()

        #define lists of edit layouts
        self.editList = [[] , []]
        self.styleList = []
        self.logicEditList    = [] #may haved to be changed due to complexity of problem

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
        self.checkChecked()

        for ind, section in enumerate(self.acceptedList):
            for i,item in enumerate(section):
                print(i)
                self.createEdit(item,ind,i,False)
        
        
        for x in self.styleList:
            self.edit_page_layout.addLayout(x)
        self.edit_page_layout.addWidget(QLabel("tst"))

        self.edit_page.setLayout(self.edit_page_layout)
        
        self.addPage(self.edit_page)
        
        #temp for testing
        
        
        self.show()        

    def createEdit(self, name, mtype, place, default):
        if mtype != 2:
            tVBox = QVBoxLayout()
            tVBox.addWidget(self.DEFAULTLIST[mtype])
            tVBox.addWidget(QLabel(name))
            eVBox = QVBoxLayout()
            eVBox.addWidget(self.NEWLIST[mtype])
            newEdit = QLineEdit()
            ddButton = IDButton(self.cur_id)
##            if not default:
##                print('1')
##                newEdit = QLineEdit().setText(name).setReadOnly(True)
##                print('2')
##                ddButton = IDButton(self.cur_id).setEnabled(False)
##            else:
##                newEdit = QLineEdit(name).setEnabled(True)
##                ddButton = IDButton(self.cur_id).setEnabled(True)
            self.cur_id += 1
            print('a')
            
            self.editList[mtype].append(newEdit)
            print('b')
            eVBox.addWidget(newEdit)
            print('c')
            aVBox = QVBoxLayout()
            print('d')
            ddButton.clicked.connect(lambda: self.makeDD(mat_vpk.getOtherFilesInDirectory("materials/"+str(self.editList[mtype][place].getText())), ddButton.id, mtype))
            print('e')
            aVBox.addWidget(ddButton)
            print('f')
            #include other methods of easing access later

            allLayout = QHBoxLayout()
            allLayout.addLayout(tVBox)
            allLayout.addLayout(eVBox)
            allLayout.addLayout(aVBox)

            
            self.styleList.append(allLayout)
            
    def makeDD(self,filelist,itemid, mt):
        #temporary
        popup = QDialog(self)
        popup.setGeometry(290,350)
        mainLO = QHBoxLayout()


        filelistwid = QListWidget()
        for file in filelist:
            filelistwid.addItem(file)
        mainLO.addWidget(filelistwid)

        filelistwid.itemClicked.connect(lambda: self.editList[mt][itemid].setText(filelistwid.currentItem()))
        popup.setLayout(mainLO)
        popup.setWindowTitle("Choose file")
        popup.exec_()
    
        
        
        
    def checkChecked(self):
        self.acceptedList = [ [] , [] , [] ]
        for i in range(3):
            for item_ind in range(self.listList[i][0].count()):
                if self.listList[i][0].item(item_ind).checkState() == Qt.Checked:
                    self.acceptedList[i].append(self.listList[i][0].item(item_ind).text().replace("\n",""))
        print(self.acceptedList)

##lists = processVMF(loadVMF())
app = QApplication(sys.argv)
f = customizeWizard("C:/Users/Anson/Desktop/shtie.vmf")
sys.exit(app.exec_())
