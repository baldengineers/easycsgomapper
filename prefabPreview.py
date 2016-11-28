from PySide.QtCore import *
from PySide.QtGui import *
import sys

#prefab info for displaying information
class prefabInfo(QDialog):
    def __init__(self, parent):
        super(prefabInfo,self).__init__()
        self.locationOrigin = parent.pos()
        self.locationAdd = parent.size()
        self.setGeometry( QRect(self.locationOrigin.x()+self.locationAdd.width()-50,
                                self.locationOrigin.y()+self.locationAdd.height()-100,
                                100,190))

        #define default values
        self.currentPrefab = ""
        self.textureList   = []
        self.heightList    = []
        self.styleList     = ["Styleless",
                              "Desert",
                              "Stone",
                              "City",
                              "Alpine"]
        self.prefabName    = ""
        #

        #create window widgets
        self.heightSpin = QSpinBox()
        self.heightSpin.setRange(0,2048)
        self.heightSpin.setValue(0)
        self.heightSpin.setSingleStep(32)
        self.heightSpin.setSuffix(" hammer units")
        
        self.styleCombo = QComboBox()
        self.styleCombo.addItems(self.styleList)

        self.prefabTitle = QLabel(self.prefabName)

        
    def updatePos():
        self.locationOrigin = parent.pos()
        self.locationAdd = parent.size()
        self.setGeometry( QRect(self.locationOrigin.x()+self.locationAdd.width()-50,
                                self.locationOrigin.y()+self.locationAdd.height()-100,
                                100,190))
