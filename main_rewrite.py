#import other modules
import sys
import os.path
import os
from PySide.QtCore import *
from PySide.QtGui import *
import importlib
from PIL import Image
from PIL.ImageQt import ImageQt
##import generateSkybox
##import light_create
##import export
import subprocess
import pickle
import random
import glob
import webbrowser
import wave
import zipfile
import shutil
import winsound

#import our own modules
import GridWidget
from classes import PrefabItem, ListGroup
import createPrefab
import pf

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #define vars used throughout class
        self.rotation = 0
        self.history = []
        self.redo_history = []

        #create window
        self.setGeometry(100, 25, 875, 750)
        self.setWindowTitle("The Mapper")
        self.setWindowIcon(QIcon("icons/icon.ico"))

        #create menubar
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.close_application)
##
##        openAction = QAction("&Open", self)
##        openAction.setShortcut("Ctrl+O")
##        openAction.setStatusTip("Open .vmf file")
##        openAction.triggered.connect(self.file_open)
##
##        saveAction = QAction("&Save", self)
##        saveAction.setShortcut("Ctrl+S")
##        saveAction.setStatusTip("Save File as .ezm save, allowing for use by others/you later.")
##        saveAction.triggered.connect(self.file_save)
##        
##        saveAsAction = QAction("&Save As", self)
##        saveAsAction.setShortcut("Ctrl+Shift+S")
##        saveAsAction.setStatusTip("Save File as .ezm save, allowing for use by others/you later.")
##        saveAsAction.triggered.connect(lambda: self.file_save(False, True))
##        
##        helpAction = QAction("&Wiki",self)
##        helpAction.triggered.connect(lambda: webbrowser.open_new_tab('http://github.com/baldengineers/easytf2_mapper/wiki'))
##        
##        tutorialAction = QAction("&Reference Guide",self)
##        tutorialAction.setStatusTip("Quick reference guide on the Mapper website.")
##        tutorialAction.triggered.connect(lambda: webbrowser.open_new_tab('http://tf2mapper.com/tutorial.html'))
##
        newAction = QAction("&New", self)
        newAction.setShortcut("Ctrl+n")
        newAction.setStatusTip("Create a New File")
        newAction.triggered.connect(self.file_new)
##
##        hammerAction = QAction("&Open Hammer",self)
##        hammerAction.setShortcut("Ctrl+H")
##        hammerAction.setStatusTip("Opens up Hammer.")
##        hammerAction.triggered.connect(lambda: self.open_hammer(0,"null"))
##
##        changeHammer = QAction("&Change Hammer Directory",self)
##        changeHammer.setShortcut("Ctrl+Shift+H")
##        changeHammer.setStatusTip("Changes default hammer directory.")
##        changeHammer.triggered.connect(lambda: self.open_hammer(0,"null",True))
##
##        changeLightAction = QAction("&Change Lighting", self)
##        changeLightAction.setShortcut("Ctrl+J")
##        changeLightAction.setStatusTip("Change the environment lighting of the map.")
##        changeLightAction.triggered.connect(self.change_light)
##        
##        exportAction = QAction("&as .VMF", self)
##        exportAction.setShortcut("Ctrl+E")
##        exportAction.setStatusTip("Export as .vmf")
##        exportAction.triggered.connect(self.file_export)
##
        undoAction = QAction("&Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.setStatusTip("Undo previous action")
        undoAction.triggered.connect(lambda: self.undo(True))

        redoAction = QAction("&Redo", self)
        redoAction.setShortcut("Ctrl+Shift+Z")
        redoAction.setStatusTip("Redo previous action")
        redoAction.triggered.connect(lambda: self.undo(False))
##
##        gridAction = QAction("&Set Grid Size", self)
##        gridAction.setShortcut("Ctrl+G")
##        gridAction.setStatusTip("Set Grid Height and Width. RESETS ALL BLOCKS.")
##        gridAction.triggered.connect(self.grid_change) #change so it just makes grid bigger/smaller, not erase all blocks, or else it would just do the same exact thing as making a new file
##
##        createPrefabAction = QAction("&Create Prefab", self)
##        createPrefabAction.setShortcut("Ctrl+I")
##        createPrefabAction.setStatusTip("View the readme for a good idea on formatting Hammer Prefabs.")
##        createPrefabAction.triggered.connect(self.create_prefab)
##
##        consoleAction = QAction("&Open Dev Console", self)
##        consoleAction.setShortcut("`")
##        consoleAction.setStatusTip("Run functions/print variables manually")
##        consoleAction.triggered.connect(self.open_console)
##
##        changeSkybox = QAction("&Change Skybox", self)
##        changeSkybox.setStatusTip("Change the skybox of the map.")
##        changeSkybox.setShortcut("Ctrl+B")
##        changeSkybox.triggered.connect(self.change_skybox)
##        
##        importPrefab = QAction("&Prefab",self)
##        importPrefab.setStatusTip("Import a prefab in a .zip file. You can find some user-made ones at http://tf2mapper.com")
##        importPrefab.setShortcut("Ctrl+Shift+I")
##        importPrefab.triggered.connect(self.import_prefab)
##
##        bspExportAction = QAction("&as .BSP",self)
##        bspExportAction.setStatusTip("Export as .bsp")
##        bspExportAction.setShortcut("Ctrl+Shift+E")
##        bspExportAction.triggered.connect(self.file_export_bsp)
##
        mainMenu = self.menuBar()
        
        
        fileMenu = mainMenu.addMenu("&File") 
        editMenu = mainMenu.addMenu("&Edit")
        optionsMenu = mainMenu.addMenu("&Options")
        toolsMenu = mainMenu.addMenu("&Tools")
        helpMenu = mainMenu.addMenu("&Help")
        
        fileMenu.addAction(newAction)
##        fileMenu.addAction(openAction)
##        fileMenu.addAction(saveAction)
##        fileMenu.addAction(saveAsAction)
##        fileMenu.addSeparator()
##        
##        importMenu = fileMenu.addMenu("&Import")
##        importMenu.addAction(importPrefab)
##
##        exportMenu = fileMenu.addMenu("&Export")
##        exportMenu.addAction(exportAction)
##        exportMenu.addAction(bspExportAction)
##        
        fileMenu.addSeparator()

        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        
        fileMenu.addAction(exitAction)
##
##        optionsMenu.addAction(gridAction)
##        optionsMenu.addAction(changeSkybox)
##        optionsMenu.addAction(changeHammer)
##        
##        toolsMenu.addAction(createPrefabAction)
##        toolsMenu.addAction(hammerAction)
##        toolsMenu.addSeparator()
##        toolsMenu.addAction(consoleAction)
##        
##        helpMenu.addAction(tutorialAction)
##        helpMenu.addAction(helpAction)

        #start default state of program
        self.home()

    def home(self):
        #grid for placing prefabs
        self.grid = GridWidget.GridWidget(20,20,self)
        self.grid_container = GridWidget.GridWidgetContainer(self.grid)
        self.grid_dock = QDockWidget("Grid", self)
        self.grid_dock.setWidget(self.grid_container)
        self.grid_dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.grid_dock)

        #define various lists
        self.tile_list1 = QListWidget()
        self.tile_list2 = QListWidget()
        self.tile_list3 = QListWidget()

        #assign lists to their specified sections
        #NOTE : add new sections to self.tab_dict and everything will update
        self.tab_dict = {"Geometry":self.tile_list1,
                         "Map Layout":self.tile_list2,
                         "Fun/Other":self.tile_list3}
        self.list_group = ListGroup([l for _, l in self.tab_dict.items()])
        for _, tile_list in self.tab_dict.items():
            tile_list.itemClicked.connect(self.set_cur_prefab)

        #add prefabs to the lists
        with open("tf2/prefabs.dat", "rb") as f:
            l = pickle.load(f)
        for p in l:
            prefab = pf.Prefab(p)
            self.tab_dict[prefab.section].addItem(PrefabItem(prefab))

        #create tabwidget for the lists
        self.list_tab_widget = QTabWidget()
        for key in self.tab_dict:
            self.list_tab_widget.addTab(self.tab_dict[key], key)

        #create dock for the tab widget
        self.prefab_dock = QDockWidget("Prefabs", self)
        self.prefab_dock.setWidget(self.list_tab_widget)
        self.prefab_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.prefab_dock)

        #create buttons for the tools
        self.grid_tools_ag = QActionGroup(self)
        self.add_prefab_action = QAction(QIcon("icons/add_prefab.png"), "Add a prefab to the grid", self.grid_tools_ag)
        self.add_prefab_action.toggled.connect(self.grid.enableAddPrefab)
        self.select_action = QAction(QIcon("icons/select_move.png"), "Select Prefabs", self.grid_tools_ag)
        self.select_action.toggled.connect(self.grid.enableSelect)
        
        self.grid_tools = QToolBar()
        self.grid_tools.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, self.grid_tools)

        for act in [self.add_prefab_action,self.select_action]:
            act.setCheckable(True)
            self.grid_tools.addAction(act)

        self.add_prefab_action.setChecked(True) #set the default button checked

    #PUT HERE ALL the functions called when a button is pressed
    #PLEASE arrange in alphabetical order
    def close_application(self):
        pass

    def create_prefab(self):
        pass

    def file_export(self):
        pass

    def file_new(self):
        dialog = GridChangeWindow(self)
        values = dialog.returnVal()
        self.grid = GridWidget.GridWidget(values[0],values[1],self)
        self.grid_container = GridWidget.GridWidgetContainer(self.grid)
        self.grid_dock.setWidget(self.grid_container)

    def file_open(self):
        pass

    def file_save(self):
        pass

    def open_hammer(self):
        pass

    def open_console(self):
        #called when the menubar button is clicked
        #allows developers to interactively determine a variety of variable values when running program
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

    # These commmands are part of the dev console 
    def sideshow(self):
        self.gif("icons/sideshow.gif", (350,262,154,103), "SIDESHOW", "icons/ss.ico")

    def heavy(self):
        self.gif("icons/heavy.gif", (350,262,150,99), "DANCE HEAVY DANCE!")

    def gif(self, file, geo, title, icon="icons\icon.ico"):
        self.gif = QLabel()
        movie = QMovie(file)
        self.gif.setMovie(movie)
        self.gif.setGeometry(geo[0],geo[1],geo[2],geo[3])
        self.gif.setWindowTitle(title)
        self.gif.setWindowIcon(QIcon(icon))
        self.gif.show()

        movie.start()
    # END
    
    def set_cur_prefab(self, item):
        #called when list item is clicked
        #assigns the current prefab of the grid to the selected prefab
        self.grid.cur_prefab = item.prefab

    def undo(self, undo):
        pass

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
            self.radioTF2.setWhatsThis("Team Fortress 2")
            self.radioCSGO = QRadioButton("&CS:GO",self)
            self.radioCSGO.setEnabled(False)
            self.radioCSGO.setWhatsThis("CS:GO mapping not yet implemented")

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
        return (self.widthSpin.value(), self.heightSpin.value())

    def closeEvent(self, event):
        if self.startup:
            sys.exit()

def main():
    #Main Program
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
    
