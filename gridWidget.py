import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GridWidget(QWidget):
    def __init__(self, spacing):
        #spacing controls how spaced out the lines are
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.setCursor(Qt.CrossCursor)
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def mousePressEvent(self, event):

        #rubber band
        if event.button() == Qt.LeftButton:
        
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):

        #rubber band
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):

        #rubber band
        if event.button() == Qt.LeftButton:
            print(QRect(self.origin, event.pos()))
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
        
