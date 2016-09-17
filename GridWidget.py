import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GridWidget(QWidget):
    def __init__(self, spacing):
        #spacing controls how spaced out the lines are
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.pList = []#list of points where gridlines intersect
        self.setCursor(Qt.CrossCursor)
        self.SetAcceptDrops(True)
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        
    def dragEnterEvent(self, e:)
        #http://www.pythonstudio.us/pyqt-programming/drag-and-drop.html
        print(e.mimeData().formats()) #for testing purposes
        
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e):
        #e.mimeData().imageData
        #multiply the image size by 32/self.spacing
        

    def mousePressEvent(self, e):

        #rubber band
        if e.button() == Qt.LeftButton:
        
            self.origin = QPoint(e.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, e):

        #rubber band
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, e.pos()).normalized())
    
    def mouseReleaseEvent(self, e):

        #rubber band
        if e.button() == Qt.LeftButton:
            print(QRect(self.origin, e.pos()))
            self.rubberBand.hide()
        
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
            
        self.pList = []
        for x in range(w/self.spacing):
            x_ind = x
            x *= self.spacing
            line = QLineF(x,0.0,x,h)
            qp.drawLine(line)
            self.plist.append([x])
            
            for y in range(h/self.spacing):
                y *= self.spacing
                line = QLineF(x,y,x+self.spacing,y)
                qp.drawLine(line)
                self.plist[x_ind].append(y)

    def setSpacing(self, spacing):
        self.spacing = spacing

def main():
    app = QApplication(sys.argv)
    grid = GridWidget(25)
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
