import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GridWidget(QWidget):
    def __init__(self, spacing=25):
        #spacing controls how spaced out the lines are
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.pList = []#list of points where gridlines intersect
        self.prefabs = [] #contains list of the prefabs in the grid, contains [icon,coordinate index for the point it is at(top left),moduleName(implement in main program)]
        self.setCursor(Qt.CrossCursor)
        self.setAcceptDrops(True)
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
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

        #rubber band
        if e.button() == Qt.RightButton:
            self.origin = self.closestP(e,"top-left")
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, e):

        #rubber band
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, self.closestP(e,"bot-right")).normalized())
    
    def mouseReleaseEvent(self, e):

        #rubber band
        if e.button() == Qt.RightButton:
            print(QRect(self.origin, self.closestP(e,"bot-right")))
            self.rubberBand.hide()

    def wheelEvent(self, e):
        if self.spacing <= 50 and self.spacing >= 5:
            e.accept
            self.changeSpacing(e.delta()/20) #replace with scrollspeed constant
        else:
            e.ignore()

        if self.spacing > 50:
            self.spacing = 50
        elif self.spacing < 10:
            self.spacing = 10

        self.repaint()
        
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
        qp.setPen(Qt.blue)
            
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

    def closestP(self, e, d):
        #finds the closest point to the mouse cursor(e) 
        #d is the direction the point is in relative to mouse cursor: "top-left", "top-right", "bot-left", "bot-right"
        for p in self.pList:
            if e.pos().x() < p.x() and e.pos().y() < p.y():
                if d == "top-left":
                    return p - QPoint(self.spacing,self.spacing)
                elif d == "top-right":
                    return p - QPoint(0,self.spacing)
                elif d == "bot-left":
                    return p - QPoint(self.spacing,0)
                elif d == "bot-right":
                    return p
                else:
                    return QPoint(0, 0)

        return QPoint(0, 0)

def main():
    app = QApplication(sys.argv)
    grid = GridWidget()
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
