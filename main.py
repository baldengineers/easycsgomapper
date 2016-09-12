#easy cs:go mapper: counter-strike: global offensive port of the easy tf2 mapper
#
#in development, not at a working stage.

#DIFFERENCES:
#more prefabrications
#more sections (subsections?)
#improved UI
#improved file count
#multi-game system
#   program boots up and variables are set which change what game the program utilizes
#   (set up after dialog with radio button + grid size is chosen)
#   grid size of createprefab, how skybox renderings, skybox textures, light vars, window titles, file directories, etc.
#move all prefabs on grid
#   if we can make a new grid system widget
#

#important:
#move all variable definitions that need changing based off game selection
#to a separate function which runs after dialog
#make the grid size dialog run before everything else. make it its own separate class that
#runs before mainwindow


import sys
#move this to after initial dialog

import os.path
import os
from PySide.QtCore import *
from PySide.QtGui import *
import importlib
import createPrefab
from PIL import Image
from PIL.ImageQt import ImageQt
import generateSkybox
import light_create
import export
import subprocess
import pickle
import pprint
import random
import glob
import webbrowser
import wave
import zipfile
import shutil
import winsound

class GridBtn(QWidget):
    def __init__(self, parent, x, y, btn_id):
        super(GridBtn, self).__init__()
        self.button = QPushButton("", parent)
        self.x,self.y = x,y
        self.btn_id = btn_id
        self.button.resize(32,32)
        self.button.setFixedSize(32, 32)
        self.button.pressed.connect(lambda: self.click_func(parent, x, y,btn_id))
        self.button.installEventFilter(self)
        self.button.show()
        self.icons = []
        for i in range(parent.levels):
            self.icons.append(None)

        parent.progress += 100/(parent.grid_x*parent.grid_y)
        parent.progressBar.setValue(parent.progress)        

    def reset_icon(self):
        self.button.setIcon(QIcon(""))

    def click_func(self, parent, x, y, btn_id, clicked=True, h_moduleName="None", h_icon=''): #h_moduleName and h_icon and h_rot are used when undoing/redoing
        current_list = eval('parent.tile_list%s' % str(parent.list_tab_widget.currentIndex()+1))

        #format | history.append((x,y,moduleName,self.icon,level))
        if clicked:
            parent.redo_history=[]
            if self.icons[parent.level]:
                moduleName = eval(parent.prefab_list[parent.list_tab_widget.currentIndex()][parent.current_list.currentRow()])
                templist=[(x,y,moduleName,self.icons[parent.level],None)]
            else:
                templist=[(x,y,None,None,None)]

        def clear_btn(btn_id):
            self.button.setIcon(QIcon())
            for l in [parent.totalblocks,parent.entity_list,parent.stored_info_list]:
                l[parent.level][btn_id] = ''
                
            parent.iconlist[parent.level][btn_id] = ('','')
            
            self.icons[parent.level] = None
        
        if self.checkForCtrl(clicked):
            clear_btn(btn_id)
        else:
            if clicked:
                if parent.ymin == None or parent.xmin == None:
                    parent.ymin,parent.xmin = y,x
                else:
                    if y < parent.ymin:
                        parent.ymin = y
                    if x < parent.xmin:
                        parent.xmin = x
                    if y > parent.ymax:
                        parent.ymax = y
                    if x > parent.xmax:
                        parent.xmax = x
                moduleName = eval(parent.prefab_list[parent.list_tab_widget.currentIndex()][parent.current_list.currentRow()])
            else:
                moduleName = h_moduleName if h_moduleName != None else clear_btn(btn_id)

            if h_moduleName != None:
                if clicked:

                    try:
                        icon = parent.gameDirVar+parent.prefab_icon_list[parent.list_tab_widget.currentIndex()][parent.current_list.currentRow()]
                        if "\n" in icon:
                            icon = icon[:-1]
                        #following three lines rotates it
                        icon = QPixmap(icon)
                        transform = QTransform().rotate(90*parent.rotation)
                        icon = icon.transformed(transform, Qt.SmoothTransformation)

                    except Exception as e:
                        print(str(e))
                        icon = parent.gameDirVar+parent.prefab_icon_list[parent.list_tab_widget.currentIndex()][current_list.currentRow()]
                        
                else:
                    icon = h_icon

                self.button.setIcon(QIcon(icon))
                self.button.setIconSize(QSize(32,32))
                parent.iconlist[parent.level][btn_id] = [parent.gameDirVar+parent.prefab_icon_list[parent.list_tab_widget.currentIndex()][current_list.currentRow()],parent.rotation]
                parent.stored_info_list[parent.level][btn_id] = [moduleName,x,y,parent.id_num,parent.world_id_num,parent.entity_num,parent.placeholder_list,parent.rotation,parent.level]

                self.icons[parent.level] = icon
            else:
                parent.stored_info_list[parent.level][btn_id] = ""

            if "*" not in parent.windowTitle():
                parent.setWindowTitle("Easy "+parent.gameVar+" Mapper* - ["+parent.currentfilename+"]")
            
            if clicked:
                templist.append((x,y,moduleName,self.icons[parent.level],None))
                parent.history.append(templist)

    def checkForCtrl(self, clicked):
        if clicked:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:           
                return True
            else: 
                return False
        else:
            return False
        
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #QApplication.setStyle(QStyleFactory.create("Cleanlooks")) #comment out if unwanted

        #define some variables used throughout the class
        self.level = 0
        self.levels = 0
        self.id_num = 1
        self.world_id_num = 2
        self.rotation = 0
        self.entity_num = 1
        self.btn_id_count = 0
        self.grid_list=[]
        self.totalblocks = []
        self.skybox_list=[]
        self.last_tuple = 'First'
        self.skybox_light_list=[]
        self.iconlist = []
        self.rotation_icon_list=[]
        self.skybox_angle_list=[]
        self.skybox_icon_list=[]
        self.prefab_list = []
        self.gridsize = []
        self.count_btns = 0
        self.entity_list=[]
        self.save_dict = {}
        self.load_dict = {}
        self.stored_info_list=[]
        self.prefab_text_list = []
        self.prefab_icon_list = []
        self.openblocks=[]
        self.placeholder_list = []
        self.history = []
        self.redo_history = []
        self.currentfilename='Untitled'
        self.file_loaded = False
        self.current_loaded = ''
        self.latest_path='/'
        self.isTF = True

        #initial startup/gridchange window
        initWindow = GridChangeWindow(self, True)
        values = initWindow.returnVal()
        
        #tell which game was chosen on launch
        if self.isTF:
            self.gameVar,self.gameDirVar = "TF2","tf2/"
        else:
            self.gameVar,self.gameDirVar = "CS:GO","csgo/"
        
        self.TFFormat() if self.isTF else self.CSFormat()
        
        util_list = [createPrefab,light_create,generateSkybox,export]
        for util in util_list:
            util.setGameDirVar(self.gameDirVar)

        #create the main window
        self.setGeometry(100, 25, 875, 750)
        self.setWindowTitle("Easy "+self.gameVar+" Mapper")
        self.setWindowIcon(QIcon("icons\icon.ico"))
        #removed for now to see how gui looks without it
##        if self.isTF:
##            namelist = ['gravelpit','2fort','upward','mvm']
##        palette = QPalette()
##        palette.setBrush(QPalette.Background,QBrush(QPixmap(self.gameDirVar+"icons/backgrounds/background_"+namelist[random.randint(0,3)]+".jpg")))
##        self.setPalette(palette)

        #create menubar
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.close_application)

        openAction = QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open .vmf file")
        openAction.triggered.connect(self.file_open)

        saveAction = QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save File as .ezm save, allowing for use by others/you later.")
        saveAction.triggered.connect(self.file_save)
        
        saveAsAction = QAction("&Save As", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.setStatusTip("Save File as .ezm save, allowing for use by others/you later.")
        saveAsAction.triggered.connect(lambda: self.file_save(False, True))
        
        helpAction = QAction("&Wiki",self)
        helpAction.triggered.connect(lambda: webbrowser.open_new_tab('http://github.com/baldengineers/easytf2_mapper/wiki'))
        
        tutorialAction = QAction("&Reference Guide",self)
        tutorialAction.setStatusTip("Quick reference guide on the Mapper website.")
        tutorialAction.triggered.connect(lambda: webbrowser.open_new_tab('http://tf2mapper.com/tutorial.html'))



        newAction = QAction("&New", self)
        newAction.setShortcut("Ctrl+n")
        newAction.setStatusTip("Create a New File")
        newAction.triggered.connect(self.grid_change)

        hammerAction = QAction("&Open Hammer",self)
        hammerAction.setShortcut("Ctrl+H")
        hammerAction.setStatusTip("Opens up Hammer.")
        hammerAction.triggered.connect(lambda: self.open_hammer(0,"null"))

        changeHammer = QAction("&Change Hammer Directory",self)
        changeHammer.setShortcut("Ctrl+Shift+H")
        changeHammer.setStatusTip("Changes default hammer directory.")
        changeHammer.triggered.connect(lambda: self.open_hammer(0,"null",True))

        changeLightAction = QAction("&Change Lighting", self)
        changeLightAction.setShortcut("Ctrl+J")
        changeLightAction.setStatusTip("Change the environment lighting of the map.")
        changeLightAction.triggered.connect(self.change_light)
        
        exportAction = QAction("&as .VMF", self)
        exportAction.setShortcut("Ctrl+E")
        exportAction.setStatusTip("Export as .vmf")
        exportAction.triggered.connect(self.file_export)

        undoAction = QAction("&Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.setStatusTip("Undo previous action")
        undoAction.triggered.connect(lambda: self.undo(True))

        redoAction = QAction("&Redo", self)
        redoAction.setShortcut("Ctrl+Shift+Z")
        redoAction.setStatusTip("Redo previous action")
        redoAction.triggered.connect(lambda: self.undo(False))

        gridAction = QAction("&Set Grid Size", self)
        gridAction.setShortcut("Ctrl+G")
        gridAction.setStatusTip("Set Grid Height and Width. RESETS ALL BLOCKS.")
        gridAction.triggered.connect(self.grid_change) #change so it just makes grid bigger/smaller, not erase all blocks, or else it would just do the same exact thing as making a new file

        createPrefabAction = QAction("&Create Prefab", self)
        createPrefabAction.setShortcut("Ctrl+I")
        createPrefabAction.setStatusTip("View the readme for a good idea on formatting Hammer Prefabs.")
        createPrefabAction.triggered.connect(self.create_prefab)

        consoleAction = QAction("&Open Dev Console", self)
        consoleAction.setShortcut("`")
        consoleAction.setStatusTip("Run functions/print variables manually")
        consoleAction.triggered.connect(self.open_console)

        changeSkybox = QAction("&Change Skybox", self)
        changeSkybox.setStatusTip("Change the skybox of the map.")
        changeSkybox.setShortcut("Ctrl+B")
        changeSkybox.triggered.connect(self.change_skybox)
        
        importPrefab = QAction("&Prefab",self)
        importPrefab.setStatusTip("Import a prefab in a .zip file. You can find some user-made ones at http://tf2mapper.com")
        importPrefab.setShortcut("Ctrl+Shift+I")
        importPrefab.triggered.connect(self.import_prefab)

        bspExportAction = QAction("&as .BSP",self)
        bspExportAction.setStatusTip("Export as .bsp")
        bspExportAction.setShortcut("Ctrl+Shift+E")
        bspExportAction.triggered.connect(self.file_export_bsp)

        mainMenu = self.menuBar()
        
        
        fileMenu = mainMenu.addMenu("&File") 
        editMenu = mainMenu.addMenu("&Edit")
        optionsMenu = mainMenu.addMenu("&Options")
        toolsMenu = mainMenu.addMenu("&Tools")
        helpMenu = mainMenu.addMenu("&Help")
        
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        
        importMenu = fileMenu.addMenu("&Import")
        importMenu.addAction(importPrefab)

        exportMenu = fileMenu.addMenu("&Export")
        exportMenu.addAction(exportAction)
        exportMenu.addAction(bspExportAction)
        
        fileMenu.addSeparator()

        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        
        fileMenu.addAction(exitAction)

        optionsMenu.addAction(gridAction)
        optionsMenu.addAction(changeSkybox)
        optionsMenu.addAction(changeHammer)
        
        toolsMenu.addAction(createPrefabAction)
        toolsMenu.addAction(hammerAction)
        toolsMenu.addSeparator()
        toolsMenu.addAction(consoleAction)
        
        helpMenu.addAction(tutorialAction)
        helpMenu.addAction(helpAction)

        #create the status bar
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        
        #perform some necessary functions for startup of program
        self.home()
        self.grid_change_func(values[0], values[1], values[2])
        self.change_skybox()
        #self.level_select()

    def TFFormat(self):
        print('TF2 version of the mapper loading!')
        sys.path.append(self.gameDirVar+"prefabs/")
        self.currentlight = '''
        entity
        {
            "id" "world_idnum"
            "classname" "light_environment"
            "_ambient" "255 255 255 100"
            "_ambientHDR" "-1 -1 -1 1"
            "_AmbientScaleHDR" "1"
            "_light" "CURRENT_LIGHT"
            "_lightHDR" "-1 -1 -1 1"
            "_lightscaleHDR" "1"
            "angles" "CURRENT_ANGLE"
            "pitch" "0"
            "SunSpreadAngle" "0"
            "origin" "0 0 73"
            editor
            {
                "color" "220 30 220"
                "visgroupshown" "1"
                "visgroupautoshown" "1"
                "logicalpos" "[0 500]"
            }
        }
        '''
        #skybox default needs to be based off game chosen
        self.skybox = 'sky_tf2_04'

        #skyboxlight = '255 255 255 200'
        #skyboxangle = '0 0 0'
        #if the user does not change the lighting, it sticks with this.
        #if the user does not choose a skybox it sticks with this

        #self.prefab_file = open(self.gameDirVar+"prefab_template/prefab_list.txt")
        #self.prefab_text_file = open(self.gameDirVar+"prefab_template/prefab_text_list.txt")
        #self.prefab_icon_file = open(self.gameDirVar+"prefab_template/prefab_icon_list.txt")
        self.prefab_file = pickle.open(self.gameDirVar+"prefabs/pinfo.ezmd")
        
        self.skybox_file = open(self.gameDirVar+"prefab_template/skybox_list.txt")
        self.skybox_icon = open(self.gameDirVar+"prefab_template/skybox_icons.txt")
        self.skybox_light = open(self.gameDirVar+"prefab_template/skybox_light.txt")
        self.skybox_angle = open(self.gameDirVar+"prefab_template/skybox_angle.txt") 

        for main_index,file in ["prefab_list","prefab_icon_list","prefab_text_list"]
            curlst = eval(file+" = [[],[],[]]")
            for index,line in self.prefab_file[main_index]:
                    self.curlst[prefab_file[3][index]].append(line[:-1] if line.endswith("\n") else line)# need to do this because reading the file generates a \n after every line
        #section=0
        '''
        self.prefab_text_list.append([])
        for line in self.prefab_text_file.readlines():
            if line == '\n':
                self.prefab_text_list.append([])
                section+=1
            else:
                self.prefab_text_list[section].append(line[:-1] if line.endswith("\n") else line)

        section=0
        self.prefab_icon_list.append([])
        for line in self.prefab_icon_file.readlines():
            if line == "\n":
                self.prefab_icon_list.append([])
                section +=1
            else:
                self.prefab_icon_list[section].append(line[:-1] if line.endswith("\n") else line)

        '''
        
        section = 0
        self.rotation_icon_list = []
        self.index_section_list = [0]
        self.rotation_icon_list.append([])

        #print(rotation_icon_list)
        for line in self.skybox_file.readlines():
            self.skybox_list.append(line[:-1] if line.endswith("\n") else line)# need to do this because reading the file generates a \n after every line

        for line in self.skybox_icon.readlines():
            self.skybox_icon_list.append(line[:-1] if line.endswith("\n") else line)

        for line in self.skybox_light.readlines():
            self.skybox_light_list.append(line[:-1] if line.endswith("\n") else line)

        for line in self.skybox_angle.readlines():
            self.skybox_angle_list.append(line[:-1] if line.endswith("\n") else line)
            
        for file in [self.prefab_file, self.prefab_text_file, self.prefab_icon_file,self.skybox_file,self.skybox_icon,self.skybox_angle,self.skybox_light]:
            file.close()

        #imports that need prefab_list to be defined
        for sec in self.prefab_list:
            for item in sec:
                if item:
                    globals()[item] = importlib.import_module(item)
                    print("import", item)
                    self.save_dict[item]=eval(item)
                    self.load_dict[eval(item)]=item

        logo = open('logo.log','r+')
        logo_f = logo.readlines()
        for i in logo_f:
            print(i[:-1])
        logo.close()

        print("\n~~~~~~~~~~~~~~~~~~~~~\nMapper loaded! You may have to alt-tab to find the input values dialog.\n")

    def CSFormat(self):
        pass

    def open_hammer(self,loaded,file,reloc = False):
        self.open_file()
        if "loaded_first_time" not in self.files or reloc:
            self.file.close()
            self.open_file(True)
            hammer_location = QFileDialog.getOpenFileName(self, "Find Hammer Location", "/","Hammer Executable (*.exe *.bat)")
            hammer_location = str(hammer_location[0])
            self.file.write("loaded_first_time\n")
            self.file.write(hammer_location)
            self.file.close()
            if loaded == 1:
                subprocess.Popen(hammer_location +" "+ file)
            else:
                subprocess.Popen(hammer_location)
        else:
            
            try:
                if loaded == 1:
                    subprocess.Popen(self.fileloaded[1] + " "+file)
                else:
                    subprocess.Popen(self.fileloaded[1])
            except Exception as e:
                print(str(e))
                self.notFound = QMessageBox()
                self.notFound.setText("ERROR!")
                self.notFound.setInformativeText("Hammer executable/batch moved or renamed!")
                self.notFound.exec_()

                self.file.close()
                os.remove(gameDirVar+"startupcache/startup.su")
                self.open_hammer(0,"null")

    def open_file(self,reloc = False):
        if reloc:
            os.remove(self.gameDirVar+"startupcache/startup.su")
        
        try:
            self.file = open(self.gameDirVar+"startupcache/startup.su", "r+")
        except:
            self.file = open(self.gameDirVar+"startupcache/startup.su", "w+")
        self.fileloaded = self.file.readlines()
        self.files = "".join(self.fileloaded)

    def closeEvent(self, event):
        #closeEvent runs close_application when the x button is pressed
        event.ignore()
        self.close_application()
        
    def home(self):
        global levels, current_list
        self.xmin = None
        self.ymin = None
        self.xmax = 0
        self.ymax = 0
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.scrollArea = QScrollArea()
        #self.scrollArea.setStyleSheet("background-color: rgb(50, 50, 50, 100);")
        #self.scrollArea.setBackgroundRole(QPalette.Light)

        #self.buttonLabel = QLabel("Rotation:",self)
        #self.levelLabel = QLabel("Level Select:",self)
        #self.listLabel = QLabel("List of prefabs:",self)
        #self.gridLabel = QLabel("Work Area:",self)
        #self.toolsLabel = QLabel("Prefab Controls:",self)

        #Add the current prefab icon
        self.current = QPushButton("",self)
        self.current.setIcon(QIcon(''))
        self.current.setIconSize(QSize(40,40))
        self.current.setFixedSize(QSize(40,40))
        self.current.setFlat(True)
        self.current.clicked.connect(self.heavy)
     
##        self.levelSelect = QComboBox(self)
##        self.levelSelect.currentIndexChanged.connect(lambda: self.change_level_new())
##
##        self.levelup = QToolButton(self)
##        self.levelup.setIcon(QIcon('icons/up.png'))
##        self.levelup.setIconSize(QSize(20,20))
##        self.levelup.clicked.connect(lambda: self.change_level(True, True))
##        self.levelup.setAutoRaise(True)
##
##        self.leveldown = QToolButton(self)
##        self.leveldown.setIcon(QIcon('icons/down.png'))
##        self.leveldown.setIconSize(QSize(20,20))
##        self.leveldown.clicked.connect(lambda: self.change_level(True, False))
##        self.leveldown.setAutoRaise(True)

        #add rotation buttons
        self.rotateCW = QToolButton(self)
        self.rotateCW.setShortcut(QKeySequence(Qt.Key_Right))
        self.rotateCW.setIcon(QIcon('icons/rotate_cw.png'))
        self.rotateCW.setIconSize(QSize(40,40))
        self.rotateCW.setFixedSize(QSize(40,40))
        self.rotateCW.setAutoRaise(True)

        self.rotateCCW = QToolButton(self)
        self.rotateCCW.setShortcut(QKeySequence(Qt.Key_Left))
        self.rotateCCW.setIcon(QIcon('icons/rotate_ccw.png'))
        self.rotateCCW.setIconSize(QSize(40,40))
        self.rotateCCW.setFixedSize(QSize(40,40))
        self.rotateCCW.setAutoRaise(True)

        #sets rotation value. 0 = right, 1 = down, 2 = left, 3 = right
        self.rotateCW.clicked.connect(self.rotateCW_func)
        self.rotateCCW.clicked.connect(self.rotateCCW_func)
        
        self.button_rotate_layout = QHBoxLayout()
        #self.button_rotate_layout.addWidget(self.buttonLabel)
        self.button_rotate_layout.addWidget(self.rotateCCW)
        self.button_rotate_layout.addWidget(self.current)
        self.button_rotate_layout.addWidget(self.rotateCW)
        #self.button_rotate_layout.addWidget(self.levelLabel)
        #self.button_rotate_layout.addWidget(self.levelSelect)
        #self.button_rotate_layout.addWidget(self.levelup)
        #self.button_rotate_layout.addWidget(self.leveldown)
        
        self.button_rotate_layout.addStretch(1)

        #add the main tool bar
        self.skyboxAction = QAction(QIcon('icons/sky.png'), "Change Skybox", self)
        self.skyboxAction.triggered.connect(self.change_skybox)

        self.tileListAction = QAction(QIcon('icons/tile_list.png'), "Re-open Tile list", self)
        self.tileListAction.triggered.connect(self.loadTileList)

        self.rotateDockAction = QAction(QIcon('icons/rotate_dock.png'), "Re-open Rotation Dock", self)
        self.rotateDockAction.triggered.connect(self.loadButtonRotate)

        self.mainToolBar = self.addToolBar("Main")
        self.mainToolBar.addAction(self.skyboxAction)
        self.mainToolBar.addAction(self.tileListAction)
        self.mainToolBar.addAction(self.rotateDockAction)
        
        #add the many sections of the tile_list    
        self.tile_list1 = QListWidget()
        self.tile_list2 = QListWidget()
        self.tile_list3 = QListWidget()
        self.current_list = self.tile_list1
                
        self.list_tab_widget = QTabWidget()
        self.list_tab_widget.setMaximumWidth(200)
        self.list_tab_widget.addTab(self.tile_list1,'Geometry')
        self.list_tab_widget.addTab(self.tile_list2,'Map Layout')
        self.list_tab_widget.addTab(self.tile_list3,'Fun')
        self.list_tab_widget.currentChanged.connect(self.changeCurrentList)

        print("len:", self.list_tab_widget.count())
        
        #add the prefab tools
        self.up_tool_btn = QToolButton(self)
        self.up_tool_btn.setIcon(QIcon('icons/up.png'))
        self.up_tool_btn.clicked.connect(self.prefab_list_up)
        
        self.down_tool_btn = QToolButton(self)
        self.down_tool_btn.setIcon(QIcon('icons/down.png'))
        self.down_tool_btn.clicked.connect(self.prefab_list_down)
        
        self.del_tool_btn = QToolButton(self)
        self.del_tool_btn.setIcon(QIcon('icons/delete.png'))
        self.del_tool_btn.clicked.connect(lambda: self.prefab_list_del(self.current_list.currentRow()))

        self.add_tool_btn = QToolButton(self)
        self.add_tool_btn.setIcon(QIcon('icons/add.png'))
        self.add_tool_btn.clicked.connect(self.create_prefab)
        
        self.tile_toolbar = QToolBar()
        for t in [self.up_tool_btn,self.down_tool_btn,self.del_tool_btn,self.add_tool_btn]:
            self.tile_toolbar.addWidget(t)
            self.tile_toolbar.addSeparator()
             
        for index, text in enumerate(self.prefab_text_list):
            for ind, indiv in enumerate(text):
                curr_list = eval("self.tile_list%d" % (index+1))
                item = QListWidgetItem(QIcon(self.gameDirVar+self.prefab_icon_list[index][ind]), indiv)
                curr_list.addItem(item)
            
        for i in range(self.list_tab_widget.count()):
            eval("self.tile_list%d" %(i+1)).currentItemChanged.connect(self.changeIcon)
        
        #contains label and list vertically
        self.tile_list_layout = QVBoxLayout()
        #self.tile_list_layout.addWidget(self.listLabel)
        self.tile_list_layout.addWidget(self.list_tab_widget)
        #self.tile_list_layout.addWidget(self.toolsLabel)
        self.tile_list_layout.addWidget(self.tile_toolbar)
        
        self.button_grid_layout = QGridLayout()
        self.button_grid_layout.setSpacing(0)
        
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.button_grid_layout)
        self.scrollArea.setWidget(self.grid_widget)
        self.scrollArea.setWidgetResizable(True)

        #contains label and grid vertically
        #need self.button_rotate_layout in a dock
        
##        self.gridLayout = QVBoxLayout()
##        self.gridLayout.addWidget(self.gridLabel)
##        self.gridLayout.addWidget(self.scrollArea)
##        self.button_grid_all = QVBoxLayout()
##        self.button_grid_all.addLayout(self.button_rotate_layout)
##        self.button_grid_all.addLayout(self.gridLayout)
        
        self.button_rotate_widget = QWidget()
        self.button_rotate_widget.setLayout(self.button_rotate_layout)
        self.tile_list_widget = QWidget()
        self.tile_list_widget.setLayout(self.tile_list_layout)

        self.loadButtonRotate()
##        self.button_rotate_dock = QDockWidget("Current Prefab", self)
##        self.button_rotate_dock.setWidget(self.button_rotate_widget)
##        self.button_rotate_dock.setFloating(True)

        self.loadTileList()
##        self.tile_list_dock = QDockWidget("Prefab List", self)
##        self.tile_list_dock.setWidget(self.tile_list_widget)
##        self.tile_list_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.tile_list_dock)
        
        self.column = QHBoxLayout()
        self.column.addWidget(self.scrollArea)
        
        self.row = QVBoxLayout(self.central_widget)
        self.row.addLayout(self.column)
        
        #widgets needed for the splitter
        #IMPLEMENT LATER
##        self.left_top = QWidget()
##        self.left_top.setLayout(self.button_rotate_layout)
##        self.left_bot = QWidget()
##        self.left_bot.setLayout(self.gridLayout)
##        self.right = QWidget()
##        self.right.setLayout(self.tile_list_layout)
##
##        self.splitter_left = QSplitter()
##        self.splitter_left.setOrientation(Qt.Vertical)
##        self.splitter_left.addWidget(self.left_top)
##        self.splitter_left.addWidget(self.left_bot)
##
##        self.splitter_right = QSplitter()
##        self.splitter_right.addWidget(self.right)
##
##        self.row = QVBoxLayout(self.central_widget)
##        self.row.addWidget(self.splitter_left)
##        self.row.addWidget(self.splitter_right)
        
        try:
            f = open(self.gameDirVar+'startupcache/firsttime.su', 'r+')
            lines = f.readlines()
        except:
            f = open(self.gameDirVar+'startupcache/firsttime.su','w+')
            lines = f.readlines()
            
        if "startup" not in lines:

            QMessageBox.information(self, "First Launch", "First Launch!\n\nYou haven't launched this before! Try looking at the <a href=\"https://github.com/baldengineers/easytf2_mapper/wiki/Texture-bug\">wiki</a> for help!")
            f.write("startup")
            f.close()
        
            #WILL ONLY WORK IN REDIST FORM
        else:
            pass
        
        
        self.show()

    def loadTileList(self):
        self.tile_list_dock = QDockWidget("Prefab List", self)
        self.tile_list_dock.setWidget(self.tile_list_widget)
        self.tile_list_dock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.tile_list_dock)
        
    def loadButtonRotate(self):
        self.button_rotate_dock = QDockWidget("Current Prefab", self)
        self.button_rotate_dock.setWidget(self.button_rotate_widget)
        self.button_rotate_dock.setFloating(True)

        self.addDockWidget(Qt.TopDockWidgetArea,self.button_rotate_dock)
        #i am.... the top dock
        
    def change_level_new(self):
        self.file_save(True)
        self.level = self.levelSelect.currentIndex()
        self.file_open(True)

    def change_level(self, but = False, up = False, undo = False):
        
        if not but:
            self.file_save(True)
            self.level = int(self.levelSelect.currentIndex()) #+1 X First level should be 0
            self.file_open(True)
            try:
                self.windowl.close()
            except:
                pass
            #self.level.setText("Level: " + str(level+1))
        if up:
            self.file_save(True)
            if self.level != self.levels-1:
                self.level = int(self.level+1)
            else:
                pass
            print(self.level)
            self.file_open(True)
            #self.level.setText("Level: " + str(level+1))
        elif not up and but:
            self.file_save(True)
            if self.level != 0:
                self.level = int(level-1)
            else:
                pass
            print(self.level)
            self.file_open(True)
            #self.level.setText("Level: " + str(level+1))            
        #change grid to grid for level

        if not undo:
            templist.append = (None,None,None,None,level)
            history.append(templist)

    def changeCurrentList(self):
        print("current list: tile_list%s" % str(self.list_tab_widget.currentIndex()+1))
        self.current_list = eval('self.tile_list%s' % str(self.list_tab_widget.currentIndex()+1))

    def rotateCW_func(self):
        if self.rotation < 3:
            self.rotation = self.rotation + 1
        else:
            self.rotation = 0
        self.changeIcon()

    def rotateCCW_func(self):
        if self.rotation == 0:
            self.rotation = 3
        else:
            self.rotation = self.rotation - 1
        self.changeIcon()

    def prefab_list_up(self):
        self.current_list = eval('self.tile_list%s' % str(self.list_tab_widget.currentIndex()+1))
        currentRow = self.current_list.currentRow()

        if currentRow > 0:
            currentItem = self.current_list.takeItem(currentRow)
            self.current_list.insertItem(currentRow - 1, currentItem)
            self.current_list.setCurrentRow(currentRow - 1)
            self.update_list_file(currentRow, currentRow - 1)
            self.changeIcon()

    def prefab_list_down(self):
        self.current_list = eval('self.tile_list%s' % str(self.list_tab_widget.currentIndex()+1))
        currentRow = self.current_list.currentRow()
        if currentRow < self.current_list.count() - 1:
            currentItem = self.current_list.takeItem(currentRow)
            self.current_list.insertItem(currentRow + 1, currentItem)
            self.current_list.setCurrentRow(currentRow + 1)
            self.update_list_file(currentRow, currentRow + 1)
            self.changeIcon()

    def update_list_file(self, old_index, new_index):

        #NEEDS TO BE REDONE
        
        file_list = [self.gameDirVar+"prefab_template/prefab_list.txt", self.gameDirVar+"prefab_template/prefab_icon_list.txt", self.gameDirVar+"prefab_template/prefab_text_list.txt"]
        list_list = [prefab_list, prefab_icon_list, prefab_text_list]

        for l in list_list:
            l.insert(new_index, l.pop(old_index))

            with open(file_list[list_list.index(l)], "w") as file:

                if list_list.index(l) == 0:   
                    rot_file = open(self.gameDirVar+"prefab_template/rot_prefab_list.txt", "w")

                for item in l:
                    file.write(item + "\n")

                    if list_list.index(l) == 0: 
                        rot_file.write(item + "_icon_list.txt" + "\n")

        #stupid icon lists, making me add more lines of code to my already concise function
         

    def prefab_list_del(self, currentprefab):

        #NEEDS TO BE REDONE based off what mode

        choice = QMessageBox.question(self,"Delete Prefab (DO NOT DELETE STOCK PREFABS)","Are you sure you want to delete \"%s\"?\nThis is mainly for developers." %(prefab_text_list[self.list_tab_widget.currentIndex()][currentprefab]),
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
           
        if choice == QMessageBox.Yes:
            text_list = [self.gameDirVar+'prefab_template/prefab_text_list.txt',self.gameDirVar+'prefab_template/rot_prefab_list.txt',
                 self.gameDirVar+'prefab_template/prefab_list.txt', self.gameDirVar+'prefab_template/prefab_icon_list.txt']

            for cur in text_list:
                file = open(cur, 'r+')
                cur_list = file.readlines()
                file.seek(0)
                file.truncate()

                print(cur_list[index_section_list[self.list_tab_widget.currentIndex()]+currentprefab+1])
                del cur_list[index_section_list[self.list_tab_widget.currentIndex()]+currentprefab+1]
                cur_str = "".join(cur_list)
                file.write(cur_str)
                file.close()
            
            restart_btn = QPushButton("Restart")
            later_btn = QPushButton("Later")
            choice = QMessageBox(self)
            choice.setIcon(QMessageBox.Question)
            choice.setWindowTitle("Prefab Successfully Deleted")
            choice.setText("Program must be restarted for changes to take effect.")
            choice.setInformativeText("Restart? You will lose any unsaved progress.")
            choice.addButton(restart_btn, QMessageBox.YesRole)
            choice.addButton(later_btn, QMessageBox.NoRole)
            choice.setDefaultButton(later_btn)

            #needs to be redone-- final redist will not be called easytf2mapper as it is no longer just that                 
            if choice.exec_() == 0:
                try:
                    subprocess.Popen('EasyTF2Mapper.exe')
                except:
                    subprocess.Popen('python main.py')
                sys.exit()
            else:
                pass
            
        else:
            del choice

    def changeIcon(self):
        icon = self.gameDirVar+self.prefab_icon_list[self.list_tab_widget.currentIndex()][self.current_list.currentRow()]

        #following three lines rotates it
        pixmap = QPixmap(icon)
        transform = QTransform().rotate(90*self.rotation)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        
        self.current.setIcon(QIcon(pixmap))
        self.current.setIconSize(QSize(32,32))
      
        
    def file_open(self, tmp = False, first = False):
        global stored_info_list, totalblocks,entity_list, currentfilename, file_loaded, latest_path,save_dict,load_dict
        if not tmp:
            name = QFileDialog.getOpenFileName(self, "Open File", latest_path,"*.ezm")
            latest_path,file = str(name[0]),open(name[0], "rb")
            self.level = 0
            self.iconlist=[]
            while True:
                header = pickle.load(file)
                if "levels" in header:
                    openlines = pickle.load(file)
                    levelcountload = openlines
                    
                elif "grid_size" in header:
                    openlines = pickle.load(file)
                    self.grid_change_func(openlines[0],openlines[1],openlines[2])
                    #print('grid changed')
                elif "stored_info_list" in header:
                    stored_info_list=[]
                    stored_info_list_temp=[]
                    openlines = pickle.load(file)
                    for item in openlines:
                        stored_info_list_temp.append(item)
                    for index,lvl in enumerate(stored_info_list_temp):
                        stored_info_list.append([])
                        for info in lvl:
                            try:
                                temp = save_dict[info[0]]
                                info[0] = temp
                                stored_info_list[index].append(info)
                            except:
                                stored_info_list[index].append('')
                elif "icon_list" in header:
                    self.iconlist=[]
                    openlines = pickle.load(file)

                    for item in openlines:
                        self.iconlist.append(item)
                  
                    
                elif "skybox2_list" in header:
                    openlines = pickle.load(file)
                    skybox2_list.setCurrentRow(openlines)
                else:
                    break
        
            for i in range(levelcountload):
                file = open(self.gameDirVar+"leveltemp/level" + str(i)+".tmp", "wb")
                pickle.dump(self.iconlist[i], file)
                file.close()
              
            #self.change_skybox()
            file.close()
            self.setWindowTitle("Easy "+gameVar+" Mapper - [" + str(name[0]) + "]")
            currentfilename = str(name[0])
            file_loaded = True
            self.upd_icns()

            
        else:
            try:
                file = open(self.gameDirVar+"leveltemp/level" + str(self.level)+".tmp", "rb")
                self.iconlist[self.level] = pickle.load(file)
                file.close()
                for index, icon in enumerate(self.iconlist[self.level]):
                    self.grid_list[index].button.setIcon(QIcon(icon))
                    self.grid_list[index].button.setIconSize(QSize(32,32))
            except Exception as e:
                print(str(e))

    def upd_icns(self):
        for index, icon in enumerate(self.iconlist[0]):
            #if "icons" in icon:
            #print(grid_list)
            try:
                #print("index: "+str(index)+" icon name: "+icon[0])
                ptrans = QTransform().rotate(90*icon[1])
                pmap = QPixmap(icon[0]).transformed(ptrans,Qt.SmoothTransformation)
                
                self.grid_list[index].button.setIcon(QIcon(pmap))
                self.grid_list[index].button.setIconSize(QSize(32,32))
            except Exception as e:
                #print(str(e))
                self.grid_list[index].button.setIcon(QIcon(''))
                self.grid_list[index].button.setIconSize(QSize(32,32))  
            
    def file_save(self, tmp = False, saveAs = False):
        global grid_x, grid_y, iconlist, levels, level, currentfilename, file_loaded, latest_path, stored_info_list, save_dict,load_dict,skybox2_list
        print(latest_path)
        self.gridsize = (grid_x,grid_y,self.levels)
        try:
            skybox_sav = skybox2_list.currentRow()
        except:
            pass
        if not tmp:
            if not file_loaded or saveAs:
                name = QFileDialog.getSaveFileName(self, "Save File", latest_path, "*.ezm")[0]
                latest_path = name
            else:
                if "*" in currentfilename:
                    name = currentfilename[:-1]
                else:
                    name = currentfilename
            file = open(name, "wb")
            pickle.dump("<levels>",file)
            pickle.dump(self.levels,file)
            pickle.dump("<grid_size>", file)
            pickle.dump(self.gridsize, file)
            pickle.dump("<stored_info_list>", file)
            stored_info_list_temp=[]
            for index,lvl in enumerate(stored_info_list):
                stored_info_list_temp.append([])
                for info in lvl:
                    #print(info)
                    try:
                        temp = load_dict[info[0]]
                        info[0] = temp
                        stored_info_list_temp[index].append(info)
                    except:
                        stored_info_list_temp[index].append('')
            pickle.dump(stored_info_list_temp, file)
            pickle.dump("<icon_list>", file)
            pickle.dump(self.iconlist, file)
            pickle.dump("<skybox>", file)
            pickle.dump(skybox_sav, file)
            file.close()
            QMessageBox.information(self, "File Saved", "File saved as %s" %(name))

            self.setWindowTitle("Easy "+gameVar+" Mapper - [" + name + "]")

            currentfilename = name
            file_loaded = True
        else:
            try:#writes tmp file to save the icons for each level
                file = open(self.gameDirVar+"leveltemp/level" + str(self.level)+".tmp", "wb")
                pickle.dump(self.iconlist[self.level], file)
                file.close()
            except Exception as e:
                
                print(str(e))
        
        

    def file_export(self,bsp=False):
        global cur_vmf_location,id_num,stored_info_list, grid_y, grid_x, world_id_num, count_btns, currentlight, skybox, skybox2_list, entity_list, skybox_light_list, skybox_angle_list, latest_path
        skyboxgeolist = []
        #make recommended height based off tallest prefab in the map
        skyboxz = QInputDialog.getText(self,("Set Skybox Height"),("Skybox Height(hammer units, %d minimum recommended):" %(1024)), QLineEdit.Normal, "%d" %(1024))
        try:
            skyboxz = int(skyboxz[0])
        except:
            QMessageBox.critical(self, "Error", "Please enter a number.")
            if bsp == False:
                self.file_export()
            else:
                self.file_export(True)
        #generate skybox stuff now
        #needs to be redone to change how skyboxes are rendered
        create = generateSkybox.createSkyboxLeft(grid_x,grid_y,skyboxz,self.id_num,world_id_num)
        skyboxgeolist.append(create[0])
        self.id_num = create[1]
        self.world_id_num = create[2]
        create = generateSkybox.createSkyboxNorth(grid_x,grid_y,skyboxz,self.id_num,world_id_num)
        skyboxgeolist.append(create[0])
        self.id_num = create[1]
        self.world_id_num = create[2]
        create = generateSkybox.createSkyboxRight(grid_x,grid_y,skyboxz,self.id_num,world_id_num)
        skyboxgeolist.append(create[0])
        self.id_num = create[1]
        self.world_id_num = create[2]
        create = generateSkybox.createSkyboxTop(grid_x,grid_y,skyboxz,self.id_num,world_id_num)
        skyboxgeolist.append(create[0])
        self.id_num = create[1]
        self.world_id_num = create[2]
        create = generateSkybox.createSkyboxSouth(grid_x,grid_y,skyboxz,self.id_num,world_id_num)
        skyboxgeolist.append(create[0])
        try:
            skybox = self.skybox_list[skybox2_list.currentRow()]
            skyboxlight = self.skybox_light_list[skybox2_list.currentRow()]
            skyboxangle = self.skybox_angle_list[skybox2_list.currentRow()]
        except:
            skyboxangle = '0 145 0'
            skyboxlight = '216 207 194 700'
            skybox = 'sky_tf2_04'

        try:
            currentlight = currentlight.replace("world_idnum",str(world_id_num))
            currentlight = currentlight.replace("CURRENT_LIGHT",skyboxlight)
            currentlight = currentlight.replace("CURRENT_ANGLE",skyboxangle)
        except:
            QMessageBox.critical(self, "Error", "Please choose a skybox.")
            self.change_skybox()
        light = currentlight
        latest_path = latest_path.replace(".ezm",".vmf")

        self.totalblocks =[]
        self.entity_list=[]
        for lvl in stored_info_list:
            for prfb in lvl:
                if prfb != '':
                    create = prfb[0].createTile(prfb[1], prfb[2], prfb[3], prfb[4], prfb[5], prfb[6], prfb[7], prfb[8])
                    self.id_num = create[1]
                    self.world_id_num = create[2]
                    self.totalblocks.append(create[0])
                    self.entity_num = create[3]
                    self.placeholder_list = create[5]
                    self.entity_list.append(create[4])
        import export #export contains the code to compile/export the map
        wholething = export.execute(totalblocks, entity_list, self.levels, skybox,skyboxgeolist, light)
              
        if bsp:
            with open(self.gameDirVar+'output/'+gameVar+'mapperoutput.vmf','w+') as f:
                f.write(wholething)
            self.cur_vmf_location = self.gameDirVar+'output/'+gameVar+'mapperoutput.vmf'
        else:
            name = QFileDialog.getSaveFileName(self, "Export .vmf", latest_path, "Valve Map File (*.vmf)")
            with open(name[0], "w+") as f:
                f.write(wholething)
            popup = QMessageBox(self, "File Exported",
                                    "The .vmf has been outputted to %s" %(name[0]) + " Open it in hammer to compile as a .bsp. Check out the wiki (https://github.com/baldengineers/easytf2_mapper/wiki/Texture-bug) for fixing errors with textures.")
            popup.setWindowTitle("File Exported")
            popup.setText("The .vmf has been outputted to %s" %(name[0]))
            popup.setInformativeText(" Open it in hammer to compile as a .bsp and/or make some changes.")
            hammerButton = popup.addButton("Open Hammer",QMessageBox.ActionRole)
            exitButton = popup.addButton("OK",QMessageBox.ActionRole)
            popup.exec_()
            if popup.clickedButton() == hammerButton:
                self.open_hammer(1,name[0])
            if popup.clickedButton() == exitButton:
                popup.deleteLater()
            self.cur_vmf_location = name[0]
 
    def file_export_bsp(self):
        self.file_export(True)
        #need to change for multi-game
        #this is fine and can be used, just make an if/then with the cs:go version
        try:
            tf2BinLoc = open(self.gameDirVar+'startupcache/vbsp.su','r+')
            tf2BinLocFile = tf2BinLoc.readlines()[0].replace('\\','/') #wtf even is this!?!? why do you need it?!?!
            tf2BinLoc.close() 

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            tf2BinLoc = open('startupcache/vbsp.su', 'w+')
            tf2BinLocFile = QFileDialog.getExistingDirectory(self,'LOCATE Team Fortress 2/bin, NOT IN DEFAULT LOCATION!')
            tf2BinLocFile = str(tf2BinLocFile.replace('\\','/'))
            tf2BinLoc.write(tf2BinLocFile)
            tf2BinLoc.close()
            
        subprocess.call('"'+tf2BinLocFile+'/vbsp.exe" "'+self.cur_vmf_location+'"')
        subprocess.call('"'+tf2BinLocFile+'/vvis.exe" "'+self.cur_vmf_location.replace('.vmf','.bsp')+'"')
        subprocess.call('"'+tf2BinLocFile+'/vrad.exe" "'+self.cur_vmf_location.replace('.vmf','.bsp')+'"')
        shutil.copyfile(cur_vmf_location.replace('.vmf','.bsp'),tf2BinLocFile.replace('/bin','/tf/maps/tf2mapperoutput.bsp'))
        popup = QMessageBox(self)
        popup.setWindowTitle("File Exported")
        popup.setText("The .vmf has been outputted to %s" %(tf2BinLocFile.replace('/bin','/tf/maps/tf2mapperoutput.bsp')))
        popup.setInformativeText("Open TF2 and in load up 'tf2outputmapper.bsp'! You can do this by typing 'map tf2mapperoutput' or by creating a server with that map.\n\nThere also is a .vmf file of your map stored in output/tf2mapperoutput.vmf.")
        hammerButton = popup.addButton("Open TF2",QMessageBox.ActionRole)
        exitButton = popup.addButton("OK",QMessageBox.ActionRole)
        popup.exec_()
        if popup.clickedButton() == hammerButton:
            subprocess.Popen('"'+tf2BinLocFile.replace('steamapps/common/Team Fortress 2/bin','')+'steam.exe" "steam://run/440"')
        if popup.clickedButton() == exitButton:
            popup.deleteLater()
            
    def removeButtons(self):

        for i in reversed(range(self.button_grid_layout.count())):
            widget = self.button_grid_layout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()
        
    def grid_change(self):
        grid_dialog = GridChangeWindow(self)
        values = grid_dialog.returnVal()
        self.grid_change_func(values[0], values[1], values[2])

    def grid_change_func(self,x,y,z):
        self.entity_list = []
        self.iconlist = []
        self.totalblocks = []
        self.grid_list = []

        self.level = 0
        self.count_btns = 0
        
        self.file_loaded = False

        self.grid_y = y
        self.grid_x = x
        self.levels = z

        self.removeButtons()

        #create the progress bar 
        self.progressBar = QProgressBar()
        self.progress = 0 #how much progress is on the progressBar
        self.status.addWidget(self.progressBar)

        for z in range(self.levels):
            self.totalblocks.append([])
            self.entity_list.append([])
            self.iconlist.append([])
            self.stored_info_list.append([])
            self.btn_id_count=0
            self.count_btns=0
        
            for x in range(self.grid_x):
                
                for y in range(self.grid_y):
                    self.totalblocks[z].append("") #This is so that there are no problems with replacing list values
                    self.entity_list[z].append("")
                    self.iconlist[z].append(('',''))
                    self.stored_info_list[z].append('')
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                grid_btn = GridBtn(self, x, y, self.btn_id_count)
                self.button_grid_layout.addWidget(grid_btn.button,y,x)
                self.btn_id_count += 1
                self.grid_list.append(grid_btn)

##                self.progress += 100/(self.grid_x*self.grid_y) MOVED TO BUTTONS' __INIT__
##                self.progressBar.setValue(self.progress)
        self.button_grid_layout.setRowStretch(self.grid_y + 1, 1)
        self.button_grid_layout.setColumnStretch(self.grid_x + 1, 1)
        self.entity_list.append("lighting slot")  
        self.count_btns = self.grid_x*self.grid_y
        self.status.removeWidget(self.progressBar)

        #self.scrollArea.deleteLater()
        #self.scrollArea = QScrollArea()
        #self.scrollArea.setBackgroundRole(QPalette.Light)
        #self.scrollArea.setStyleSheet("background-color: rgb(50, 50, 50, 100);")


##        self.grid_widget = QWidget()
##        self.grid_widget.setLayout(self.button_grid_layout)
##        self.scrollArea.setWidget(self.grid_widget)
##        self.scrollArea.ensureWidgetVisible(self.grid_widget)
##        self.scrollArea.setWidgetResizable(True)

        for i in range(self.levels):
            with open(self.gameDirVar+"leveltemp/level" + str(i)+".tmp", "wb") as f:
                pickle.dump(self.iconlist[i], f)
        
        #self.gridLayout.addWidget(self.scrollArea)
        #self.button_grid_all.addLayout(self.gridLayout)
        self.setWindowTitle("Easy "+self.gameVar+" Mapper ")

    def change_light(self):
        
        r_input = QInputDialog.getText(self, ("Red light level 0-255"),
                                       ("Put in the red light ambiance level, 0-255:"))
        g_input = QInputDialog.getText(self, ("Green light level 0-255"),
                                       ("Put in the green light ambiance level, 0-255:"))
        b_input = QInputDialog.getText(self, ("Blue light level 0-255"),
                                       ("Put in the blue light ambiance level, 0-255:"))
        light_input = QInputDialog.getText(self, ("Brightness level"),
                                       ("Put in the brightness level desired:"))
        try:
            
            r_input = int(r_input[0])
            g_input = int(g_input[0])
            b_input = int(b_input[0])
            light_input = int(light_input[0])
            if r_input > 255 or g_input > 255 or b_input > 255:
                print("Error. Put in a number below 256 for each color input")
            else:
                pass
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a number.")
            self.change_light()

        self.currentlight = light_create.replacevalues(r_input,g_input,b_input,light_input,world_id_num)

    def change_skybox(self):
        self.window = QDialog(self)
        skybox2_list = QListWidget()
        skybox2_list.setIconSize(QSize(200, 25))
        for index, text in enumerate(self.skybox_list):
            item = QListWidgetItem(QIcon(self.gameDirVar+self.skybox_icon_list[index]), text)
            skybox2_list.addItem(item)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(skybox2_list)
        self.window.setGeometry(150,150,400,300)
        self.window.setWindowTitle("Choose a skybox")
        self.window.setWindowIcon(QIcon("icons\icon.ico"))

        self.window.setLayout(self.layout)
        skybox2_list.itemClicked.connect(self.window.close)
        self.window.exec_()

    def close_application(self, restart = False):
        if not restart:
            close = True
            
            if "*" in self.windowTitle():
                print('are you sure')
                choice = QMessageBox.warning(self, "Exit TF2Mapper",
                                              "Some changes have not been saved.\nDo you really want to quit?",
                                              QMessageBox.Ok | QMessageBox.Cancel,
                                              QMessageBox.Cancel)
                if choice != QMessageBox.Ok:
                    close = False
                
            if close:
                folder = self.gameDirVar+'leveltemp/'
                for f in os.listdir(folder):
                    if "level" in f: 
                        print("removing", f)
                        os.remove(folder+f)
                    
                sys.exit()
            else:
                pass
        if restart:
            choice = QMessageBox.question(self, "Restart",
                                          "Are you sure you want to restart?",
                                          QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            if choice == QMessageBox.Yes:
                folder = self.gameDirVar+'leveltemp/'
                for f in os.listdir(folder):
                    if "level" in f: 
                        print("removing", f)
                        os.remove(folder+f)
                #again the exe references need to be changed    
                try:
                    subprocess.call('sudo wine EasyTF2Mapper.exe')
                    
                except:
                    try:
                        subprocess.Popen('EasyTF2Mapper.exe')
                    except:
                        subprocess.Popen('python main.py')
                sys.exit()
            else:
                pass

    def create_prefab(self):
        
        self.window = QDialog(self)
        self.textLineEdit = QLineEdit()
        self.nameLineEdit = QLineEdit()
        
        self.vmfTextEdit = QLineEdit()
        self.iconTextEdit = QLineEdit()
        
        self.vmfBrowse = QPushButton("Browse",self)
        self.vmfBrowse.clicked.connect(lambda: self.vmfTextEdit.setText(QFileDialog.getOpenFileName(self, "Choose .vmf File", "/","*.vmf")[0]))
        
        self.iconBrowse = QPushButton("Browse",self)
        self.iconBrowse.clicked.connect(lambda: self.iconTextEdit.setText(QFileDialog.getOpenFileName(self, "Choose .jpg File", "/","*.jpg")[0]))

        self.vmfLayout = QHBoxLayout()
        self.vmfLayout.addWidget(self.vmfTextEdit)
        self.vmfLayout.addWidget(self.vmfBrowse)
        self.vmfBrowse.setWindowModality(Qt.NonModal)
        
        self.iconLayout = QHBoxLayout()
        self.iconLayout.addWidget(self.iconTextEdit)
        self.iconLayout.addWidget(self.iconBrowse)

        self.okay_btn = QPushButton("Create Prefab", self)

        self.blankstring = QWidget()

        self.okay_btn_layout = QHBoxLayout()
        self.okay_btn_layout.addStretch(1)
        self.okay_btn_layout.addWidget(self.okay_btn)

        self.okay_btn.clicked.connect(self.create_run_func)

        #self.rotCheckBox = QCheckBox()
        self.expCheckBox = QCheckBox()
        self.buggyText = QLabel("This is a pretty buggy tool at this point, and is mostly used by developers. Are you sure you want to do this? \n(exported prefabs can be found in the main directory, where the executable is.)")

        self.sectionSelect = QComboBox()
        #needs to have a cs:go version
        if self.isTF:
            self.sectionSelect.addItems(["Geometry","Map Layout","Fun/Other"])
        else:
            pass
        self.radioLayout = QHBoxLayout()
        self.radioTF2 = QRadioButton("TF2",self)
        self.radioCSGO = QRadioButton("CS:GO",self)
        self.group.addButton(self.radioTF2)
        self.group.addButton(self.radioCSGO)
        self.group.setExclusive(True)
        self.radioLayout.addWidget(self.radioTF2)
        self.radioLayout.addWidget(self.radioCSGO)
        
        self.form = QFormLayout()
        self.form.addRow(self.buggyText)
        self.form.addRow("Prefab Text:", self.textLineEdit)
        self.form.addRow("Prefab Name:", self.nameLineEdit)
        self.form.addRow("VMF file (.vmf):", self.vmfLayout)
        self.form.addRow("Icon (.jpg):", self.iconLayout)
        #self.form.addRow("Make Rotations?", self.rotCheckBox)
        self.form.addRow("Export prefab?", self.expCheckBox)
        self.form.addRow("Which section?",self.sectionSelect)
        self.form.addRow("Which game?", self.radioLayout)
        for i in range(5):
            self.form.addRow(self.blankstring)
        self.form.addRow(self.okay_btn_layout)

        
        self.window.setGeometry(150,150,400,300)
        self.window.setWindowTitle("Create Prefab")
        self.window.setWindowIcon(QIcon("icons\icon.ico"))

        self.window.setLayout(self.form)
        self.window.exec_()

    def create_run_func(self):
        if self.sectionSelect.currentIndex() == 2:
            input_number = 'END'
        else:
            input_number = index_section_list[self.sectionSelect.currentIndex()+1]
        name_str = self.nameLineEdit.displayText().replace(' ','_')
        form_list,t_list = [self.vmfTextEdit.displayText(),self.textLineEdit.displayText(),self.iconTextEdit.displayText(),self.nameLineEdit.displayText()],[]
        form_dict = {1:'Prefab Text',2:'Prefab Name',3:'VMF file',4:'Icon'}
        if self.vmfTextEdit.displayText() !=  '' and self.textLineEdit.displayText() != '' and self.iconTextEdit.displayText() != '' and self.nameLineEdit.displayText() != '':
            QMessageBox.information(self, "Files Created, restart to see the prefab.",createPrefab.create(self.vmfTextEdit.displayText(), name_str, self.textLineEdit.displayText(), self.iconTextEdit.displayText(),self.expCheckBox.isChecked(),input_number,self.sectionSelect.currentIndex(),self.radioTF2.isChecked()))
            restart_btn = QPushButton("Restart")
            later_btn = QPushButton("Later")
            choice = QMessageBox(self)
            choice.setIcon(QMessageBox.Question)
            choice.setWindowTitle("Prefab Successfully Created")
            choice.setText("Program must be restarted for changes to take effect.")
            choice.setInformativeText("Restart? You will lose any unsaved progress.")
            choice.addButton(restart_btn, QMessageBox.YesRole)
            choice.addButton(later_btn, QMessageBox.NoRole)
            choice.setDefaultButton(later_btn)
            #exe name change
            if choice.exec_() == 0:
                try:
                    subprocess.call('sudo wine EasyTF2Mapper.exe')
                    
                except:
                    try:
                        subprocess.Popen('EasyTF2Mapper.exe')
                    except:
                        subprocess.Popen('python main.py')
                sys.exit()
            else:
                pass  
        else:
            for index,box in enumerate(form_list):         
                if box == '':          
                    t_list.append(form_dict[index+1])
            err = ", ".join(t_list)
            QMessageBox.critical(self, "Error", "Fill out all sections of the form. ("+err+")")
        #self.importprefabs()

    def import_prefab(self):
        name = QFileDialog.getOpenFileName(self, "Import Zipped Prefab", latest_path,"*.zip")[0]
        prefab_zip = zipfile.ZipFile(name).extractall("")

        with open("info.txt", "r+") as f:
            zip_info = f.readlines()
            if zip_info[3] == 2:
                with open(self.gameDirVar+'prefab_template/rot_prefab_list.txt',"a") as d:
                    tempfil = zip_info[0]
                    tempfil = tempfil.replace('\n','')
                    d.write(self.gameDirVar+tempfil+"_icon_list.txt\n")
                with open(self.gameDirVar+'prefab_template/prefab_list.txt',"a") as d:
                    tempfil = zip_info[0]
                    tempfil = tempfil.replace('\n','')
                    d.write(tempfil+'\n')
                with open(self.gameDirVar+'prefab_template/prefab_text_list.txt',"a") as d:
                    d.write(zip_info[2])
                with open(self.gameDirVar+'prefab_template/prefab_icon_list.txt',"a") as d:
                    tempfil = zip_info[1]
                    tempfil = tempfil.replace('\n','')
                    d.write(self.gameDirVar+'icons/'+tempfil+'_right.jpg\n')
            else:
                #most childish code 2016
                z = open(self.gameDirVar+'prefab_template/rot_prefab_list.txt',"r")
                zlines = z.readlines()
                z.close()
                y = open(self.gameDirVar+'prefab_template/prefab_list.txt',"r")
                ylines = y.readlines()
                y.close()
                x = open(self.gameDirVar+'prefab_template/prefab_text_list.txt',"r")
                xlines = x.readlines()
                x.close()
                w = open(self.gameDirVar+'prefab_template/prefab_icon_list.txt',"r")
                wlines = w.readlines()
                w.close()
                
                z = open(self.gameDirVar+'prefab_template/rot_prefab_list.txt',"w")
                zlines.insert(self.index_section_index[int(zip_info[3])]-1,self.gameDirVar+zip_info[0]+"_icon_list.txt\n")
                zlines = "".join(zlines)
                z.write(zlines)
                z.close()
                y = open(self.gameDirVar+'prefab_template/prefab_list.txt',"w")
                ylines.insert(self.index_section_index[int(zip_info[3])]-1,zip_info[0])
                ylines = "".join(ylines)
                y.write(ylines)
                y.close()
                x = open(self.gameDirVar+'prefab_template/prefab_text_list.txt',"w")
                xlines.insert(self.index_section_index[int(zip_info[3])]-1,zip_info[2])
                xlines = "".join(xlines)
                x.write(xlines)
                x.close()
                w = open(self.gameDirVar+'prefab_template/prefab_icon_list.txt',"w")
                wlines.insert(self.index_section_index[int(zip_info[3])]-1,'icons/'+zip_info[1]+'_right.jpg\n')
                wlines = "".join(wlines)
                w.write(wlines)
                w.close()                

        os.remove("info.txt")
        
        restart_btn = QPushButton("Restart")
        later_btn = QPushButton("Later")
        choice = QMessageBox(self)
        choice.setIcon(QMessageBox.Question)
        choice.setWindowTitle("Prefab Successfully Imported")
        choice.setText("Program must be restarted for changes to take effect.")
        choice.setInformativeText("Restart? You will lose any unsaved progress.")
        choice.addButton(restart_btn, QMessageBox.YesRole)
        choice.addButton(later_btn, QMessageBox.NoRole)
        choice.setDefaultButton(later_btn)
        #rename exe
        if choice.exec_() == 0:
            try:
                subprocess.call('sudo wine EasyTF2Mapper.exe')
            except:
                try:
                    subprocess.Popen('EasyTF2Mapper.exe')
                except:
                    subprocess.Popen('python main.py')
            sys.exit()
        else:
            pass  
        

    def open_console(self):
        #contains dev console where you can manually run functions

        self.console = QDialog()
        self.console.setWindowTitle("Developer Console")

        self.prev_text = QTextEdit("<Bald Engineers Developer Console>")
        self.prev_text.setText('''Developer console for Easy '''+gameVar+''' Mapper version r 1.0.1. Current commands are:
print <variable>, setlevel <int>, help, restart, exit, func <function>, wiki, py <python function>.\n''')
        self.prev_text.setReadOnly(True)
        
        self.curr_text = QLineEdit()
        self.curr_text_btn = QPushButton("Enter")
        self.curr_text_btn.clicked.connect(self.console_enter)
        
        self.curr_text_layout = QHBoxLayout()
        self.curr_text_layout.addWidget(self.curr_text)
        self.curr_text_layout.addWidget(self.curr_text_btn)
        
        self.console_close_btn = QPushButton("Close")
        self.console_close_btn.clicked.connect(self.console.close)
        
        self.console_form = QFormLayout()
        self.console_form.addRow(self.prev_text)
        self.console_form.addRow(self.curr_text_layout)
        self.console_form.addRow(self.console_close_btn)

        
        self.console.setLayout(self.console_form)
        self.console.show()

    def console_enter(self):
        global level, levels
        
        command = ""
        char_num = 0
        text = self.curr_text.displayText()
        text_prefix = text + " --> "
        
        command = text.split()[0]
        
        try:
            value = text.split()[1]
        except IndexError:
            value = ""

        if command == "print":

            try:
                new_text = text_prefix + str(eval(value))
            except Exception as e:
                new_text = text_prefix + str(e)

        elif command == "setlevel":
            try:
                if int(value)-1 < int(self.levels):
                    self.level = int(value)-1
                    self.level.setText("Level: " + str(self.level+1))
                    new_text = text_prefix + "Level set to "+str(value+".")
                else:
                    new_text = text_prefix + "Level "+str(value+" is out of range.")
            except Exception as e:
                new_text = text_prefix + str(e)

        elif command == "help":
            new_text = text_prefix + '''Developer console for Easy '''+gameVar+''' Mapper version r 1.0.1. Current commands are: print <variable>, func <function>, setlevel <int>, help, restart, exit, func <function>, wiki, py <python function>'''

        elif command == "exit":
            self.close_application()
            
        elif command == "restart":
            self.close_application(True)

        elif command == "pootis":
            new_text = '<img src="icons/thedoobs.jpg">'

        elif command == "sterries" or command == "jerries":
            new_text = text_prefix + "Gimme all those berries, berries, berries!"
            

        elif command == "sideshow":
            new_text = ''
            self.sideshow()
        elif command == "func":
            try:
                eval("self."+value + "()")
                new_text = text_prefix + "Function "+value+" has been run."
            except Exception as e:
                new_text = text_prefix + str(e)

        elif command == "wiki":
            try:
                webbrowser.open("http://github.com/baldengineers/easytf2_mapper/wiki")
                new_text = text_prefix + "Wiki has been opened in your default browser"
            except Exception as e:
                print(str(e))
                
        elif command == "py":
            try:
                new_text = text_prefix + str(eval(value))
            except Exception as e:
                new_text = text_prefix + str(e)
        else:
            new_text = text_prefix + "\"" + command + "\" is not a valid command"

        self.prev_text.append(new_text)
        self.curr_text.setText("")

    def undo(self, undo):
        if self.history if undo else self.redo_history:
            x = self.history[-1][0][0] if undo else self.redo_history[-1][1][0]
            y = self.history[-1][0][1] if undo else self.redo_history[-1][1][1]
            h_moduleName = self.history[-1][0][2] if undo else self.redo_history[-1][1][2]
            h_icon = self.history[-1][0][3] if undo else self.redo_history[-1][1][3]
            h_level = self.history[-1][0][4] if undo else self.redo_history[-1][1][4]

            if h_level == None:   
                for button in self.grid_list:
                    if button.x == x and button.y == y:
                        button.click_func(self, x, y, button.btn_id, False, h_moduleName, h_icon)
                        break
            else:
                #self.level.setText("Level: " + str(h_level+1))
                self.levellist.setCurrentRow(h_level)
                self.change_level(False, False, True)

            self.redo_history.append(self.history.pop(-1)) if undo else self.history.append(self.redo_history.pop(-1))
        else:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        
        #format | click_func(parent, x, y, btn_id, clicked=True, h_moduleName="None", h_icon='')
        #format | history.append((x,y,moduleName,self.icon,level), (x,y,moduleName,self.icon,level))

    def sideshow(self):
        self.gif("icons/sideshow.gif", (350,262,154,103), "SIDESHOW", "icons/ss.ico")

    def heavy(self):
        self.gif("icons/heavy.gif", (350,262,150,99), "DANCE HEAVY DANCE!")
        print("LOL")

    def gif(self, file, geo, title, icon="icons\icon.ico"):
        self.gif = QLabel()
        movie = QMovie(file)
        self.gif.setMovie(movie)
        self.gif.setGeometry(geo[0],geo[1],geo[2],geo[3])
        self.gif.setWindowTitle(title)
        self.gif.setWindowIcon(QIcon(icon))
        self.gif.show()

        movie.start()

class GridChangeWindow(QDialog):
    def __init__(self, parent, startup = False):
        super(GridChangeWindow,self).__init__()
        #parent - references the main window's attributes
        #startup | Boolean | - if the window is being run when program starts up

        self.startup = startup
        
        if not self.startup:
            parent.entity_list = []
            parent.iconlist = []
            parent.totalblocks = []
            parent.grid_list = []

        self.widthSpin = QSpinBox()
        self.heightSpin = QSpinBox()

        for spin in [self.widthSpin, self.heightSpin]:
            spin.setRange(0,1000)
            spin.setSingleStep(5)
            spin.setValue(5)
        
        self.okay_btn = QPushButton("OK",self)
        self.okay_btn.clicked.connect(lambda: self.clickFunction(parent))

        self.form = QFormLayout()
        self.form.addRow("Set Grid Width:",self.widthSpin)
        self.form.addRow("Set Grid Height:",self.heightSpin)
        #self.form.addRow("Set Amount of Levels:",self.text3)
        if self.startup:
            self.radioTF2 = QRadioButton("&TF2",self)
            self.radioTF2.setChecked(True)
            self.radioTF2.setWhatsThis("TF2- The best game xd")
            self.radioCSGO = QRadioButton("&CS:GO",self)

            self.group = QButtonGroup()
            self.group.addButton(self.radioTF2)
            self.group.addButton(self.radioCSGO)
            self.group.setExclusive(True)

            self.radioLayout = QHBoxLayout()
            self.radioLayout.addWidget(self.radioTF2)
            self.radioLayout.addWidget(self.radioCSGO)
            
            self.form.addRow("Choose game:",self.radioLayout)
        self.form.addRow(self.okay_btn)

        self.setLayout(self.form)
        self.setWindowTitle("Set Grid Size")
        self.setWindowIcon(QIcon("icons\icon.ico"))
        self.exec_()

    def clickFunction(self, parent):
        self.hide()
        self.deleteLater()
        if self.startup:
            parent.isTF = self.radioTF2.isChecked()

    def returnVal(self):
        return (self.widthSpin.value(), self.heightSpin.value(), 1)

    def closeEvent(self, event):
        if self.startup:
            sys.exit()

#Main Program
app = QApplication(sys.argv)
main = MainWindow()
app.exec_()

