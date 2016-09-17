import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GridWidget(QWidget):
    def __init__(self, spacing):
        #spacing controls how spaced out the lines are
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.setCursor(Qt.CrossCursor)
        self.SetAcceptDrops(True)
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        
    def dragEnterEvent(self, e):
        #http://www.pythonstudio.us/pyqt-programming/drag-and-drop.html
        print(e.mimeData().formats) #for testing purposes
        
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e):
        #e.mimeData().imageData
        

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
        
        while x <= w:
            line = QLineF(x,0.0,x,h)
            qp.drawLine(line)
            x += self.spacing

        while y <= h:
            line = QLineF(0.0,y,w,y)
            qp.drawLine(line)
            y += self.spacing

    def setSpacing(self, spacing):
        self.spacing = spacing

def main():
    app = QApplication(sys.argv)
    grid = GridWidget(25)
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
