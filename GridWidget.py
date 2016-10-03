import sys
from PySide.QtCore import *
from PySide.QtGui import *
import main

class GridWidget(QWidget):
    def __init__(self, spacing=25):
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.pList = []
        self.setCursor(Qt.CrossCursor)
        
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        #draw the grid
        x, y = 0, 0
        qp.setPen(Qt.lightGray)
            
        coors = []
        for x in range(int(w/self.spacing)+1):
            x_ind = x
            x *= self.spacing
            line = QLineF(x,0.0,x,h)
            qp.drawLine(line)
            
            for y in range(int(h/self.spacing)+1):
                y *= self.spacing
                line = QLineF(x,y,x+self.spacing,y)
                qp.drawLine(line)
                coors.append([x,y])

        self.pList = []
        for c in coors:
            p = QPoint(c[0],c[1])
            self.pList.append(p)
        #print(self.pList)

    def setSpacing(self, spacing):
        self.spacing = spacing

    def changeSpacing(self, spacing):
        self.spacing += spacing

    def closestP(self, e):
        #finds the closest point to the mouse cursor(e)
        dist = []
        #print(e.pos())
        for p in self.pList:
            dist.append([abs(e.pos().x() - p.x()),abs(e.pos().y() - p.y())])
        xy = min(d for d in dist)
        return self.pList[dist.index(xy)]

class MainGridWidget(GridWidget):
    #This is the grid for the main program, where you place the prefabs
    def __init__(self, spacing=25, parent=None):
        #spacing controls how spaced out the lines are
        super(MainGridWidget, self).__init__(spacing)
        self.parent = parent
        #self.spacing = spacing #commented out because using the parameter in init function above should do the same thing
        self.pList = []#list of points where gridlines intersect
        self.prefabs = [] #contains list of the prefabs in the grid, contains [icon,coordinate index for the point it is at(top left),moduleName(implement in main program)]
        self.setCursor(Qt.CrossCursor)
        self.setAcceptDrops(True)
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        #self.rubberBand = Selection(self)
        self.origin = QPoint()
        
    def dragEnterEvent(self, e):
        #http://www.pythonstudio.us/pyqt-programming/drag-and-drop.html
        
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        pass
    
    def dropEvent(self, e):
        #e.mimeData().imageData
        #multiply the image size by 32/self.spacing
##        for p in self.pList:
##            if e.pos().x() < p.x() and e.pos().y() < p.y():
##                coor_ind = self.pList.index(QPoint(p.x() - self.spacing, p.y() - self.spacing))
##                break

##        self.prefabs.append([e.mimeData().imageData(), coor])
##        print(e.mimeData().imageData())
        pass

    def mousePressEvent(self, e):

        if e.button() == Qt.RightButton:
            self.origin = self.closestP(e)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.setShowImage(False)
            self.rubberBand.show()
        elif e.button() == Qt.LeftButton:
            #self.parent.cur_icon
            pass
    
    def mouseMoveEvent(self, e):

        #rubber band
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, self.closestP(e)).normalized())
    
    def mouseReleaseEvent(self, e):

        if e.button() == Qt.LeftButton:
            pass   
        #rubber band
        elif e.button() == Qt.RightButton:
            print(QRect(self.origin, self.closestP(e)))
            self.rubberBand.hide()

    def wheelEvent(self, e):
        if self.spacing <= 50 and self.spacing >= 16:
            e.accept()
            self.changeSpacing(e.delta()/20) #replace with scrollspeed constant
        else:
            e.ignore()

        if self.spacing > 50:
            self.spacing = 50
        elif self.spacing < 16:
            self.spacing = 16

        print(self.spacing)

        self.repaint()

class CreatePrefabGridWidget(GridWidget):
    def __init__(self, spacing=25):
        super(CreatePrefabGridWidget, self).__init__(spacing)

"""
class Selection(QRubberBand):
    def __init__(self, parent):
        super(Selection, self).__init__(QRubberBand.Rectangle, parent)
        self.showImage = False #whether to display the prefab icon while selecting
        self.pixmap = None

    def setShowImage(self, image):
        self.showImage = image

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        print(self.pixmap.rect())
    
    def paintEvent(self, e):
        qp = QPainter()
        pen = QPen(Qt.black)
        pen.setWidth(5)
        pen.setStyle(Qt.DashLine)
        if self.showImage:
            pScaled = self.pixmap.scaled(e.rect().width(), e.rect().height(), Qt.KeepAspectRatio)
            #pRect.setSize(QSize(e.rect().width(),e.rect().height()))
            brush = QBrush(Qt.green, pScaled)
        else:
            brush = QBrush(Qt.white)

        qp.begin(self)
        qp.setPen(pen)
        qp.setOpacity(0.5)
        qp.setBrush(brush)
        qp.drawRect(e.rect())
        qp.end()
"""

def main():
    app = QApplication(sys.argv)
    grid = GridWidget()
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
