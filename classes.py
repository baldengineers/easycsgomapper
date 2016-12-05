from PySide.QtCore import *
from PySide.QtGui import *

class PrefabItem(QListWidgetItem):
    def __init__(self, prefab, parent=None):
        super(PrefabItem, self).__init__(prefab.text, parent)

        self.prefab = prefab

class ListGroup():
    def __init__(self, group):
        #only allows one item to be selected at a time in the list widgets
        for l in group:
            l.itemClicked.connect(lambda: self.deselect([i for i in group if i != l]))

    def deselect(self, lists):
        for l in lists:
            l.clearSelection()
