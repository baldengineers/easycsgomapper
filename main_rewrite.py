#import other modules

##import generateSkybox
##import light_create
##import export
from PIL import Image
from PIL.ImageQt import ImageQt
from PySide.QtCore import *
from PySide.QtGui import *
import collections
import glob
import importlib
import os
import os.path
import pickle
import random
import shutil
import subprocess
import sys
import wave
import webbrowser
import winsound
import zipfile

#import our own modules
from GridWidget import GridWidget, GridWidgetContainer
from classes import PrefabItem, ListGroup
from console import Console
import createPrefab
import pf

class MainWindow(QMainWindow):
    VERSION = "1.0.2"
    
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

        openAction = QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open .vmf file")
        openAction.triggered.connect(self.file_open)

        saveAction = QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save File as .ezm save, allowing for use by others/you later.")
        saveAction.triggered.connect(self.file_save)
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
##        createPrefabAction = QAction("&Create Prefab", self)
##        createPrefabAction.setShortcut("Ctrl+I")
##        createPrefabAction.setStatusTip("View the readme for a good idea on formatting Hammer Prefabs.")
##        createPrefabAction.triggered.connect(self.create_prefab)
##
        consoleAction = QAction("&Open Dev Console", self)
        consoleAction.setShortcut("`")
        consoleAction.setStatusTip("Run functions/print variables manually")
        consoleAction.triggered.connect(self.open_console)
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
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
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
        toolsMenu.addAction(consoleAction)
##        
##        helpMenu.addAction(tutorialAction)
##        helpMenu.addAction(helpAction)

        #start default state of program
        self.home()

    def home(self):
        #grid for placing prefabs
        self.grid = GridWidget(20,20,self)
        self.grid_container = GridWidgetContainer(self.grid)
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
        self.tab_dict = collections.OrderedDict(
                        [("Geometry",   self.tile_list1),
                         ("Map Layout", self.tile_list2),
                         ("Fun/Other",  self.tile_list3)]
                        )
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

    #Define events here
    def closeEvent(self, event):
        #closeEvent runs close_application when the x button is pressed
        event.ignore()
        self.close_application()

    #PUT HERE ALL the functions called when a button is pressed
    #PLEASE arrange in alphabetical order
    def close_application(self):
        sys.exit()

    def create_prefab(self):
        pass

    def file_export(self):
        pass

    def file_new(self):
        dialog = GridChangeWindow(self)
        values = dialog.returnVal()
        self.grid = GridWidget(values[0],values[1],self)
        self.grid_container = GridWidgetContainer(self.grid)
        self.grid_dock.setWidget(self.grid_container)

    def file_open(self):
        name = QFileDialog.getOpenFileName(self, "Open File", 'user/saves/', "*.ezm")[0]

        with open(name, "rb") as f:
            print(pickle.load(f))
            
        
    def file_save(self):
        name = QFileDialog.getSaveFileName(self, "Save File", 'user/saves/', "*.ezm")[0]
        data = [self.grid.prefabs] #add more to this as more things must be saved, e.g. skybox
        
        with open(name, "wb") as f:
            pickle.dump(data, f)

    def open_hammer(self):
        pass

    def open_console(self):
        #called when the menubar button is clicked
        #allows developers to interactively determine a variety of variable values when running program
        self.console = Console(self)
    
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
    
