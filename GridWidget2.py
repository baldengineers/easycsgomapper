import sys
import math
from PySide.QtCore import *
from PySide.QtGui import *

X,Y = 0,1

class GridWidget(QWidget):
    def __init__(self, x, y, rband=True):
        super(GridWidget, self).__init__()
        self.x = x
        self.y = y
        self.draw_list = []
        #self.startX = 0
        #self.startY = 0
        #self.setMouseTracking(True)
        self.spacing = 2
        self.grid_width = 16
        self.grid_list = []
        #vars for rubber band
        self.rband = rband #if rubberband is enabled
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

##    def sizeHint(self):
##        w = self.x*self.spacing + self.x*self.grid_width
##        h = self.y*self.spacing + self.y*self.grid_width
##        return QSize(w,h)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
##        size = self.size()
##        w = size.width()
##        h = size.height()
        
        qp.setPen(QColor(0, 0, 0, 0))
        qp.setBrush(QColor(200, 200, 200, 200))
        
        for x in range(0, self.x*self.grid_width, self.grid_width):
            x += self.spacing*x/self.grid_width
            for y in range(0, self.y*self.grid_width, self.grid_width):
                y += self.spacing*y/self.grid_width
                self.grid_list.append(GridSquare(x, y, self.grid_width, self.grid_width))
                qp.drawRect(self.grid_list[-1])

        w = self.x*self.spacing + self.x*self.grid_width
        h = self.y*self.spacing + self.y*self.grid_width
        self.setFixedSize(QSize(w, h))
        
        ##Draw the Prefabs
        
        for prefab in draw_list:
            QPolygon([QPoint(prefab[X]*(self.spacing+self.grid_width) + prefab[2][p][X], prefab[Y]*(self.spacing+self.grid_width) + prefab[2][p][X])])
            
    def updatePrefabs(self, x, y, prefab):
        #prefab is a list of the points in its icon
        self.draw_list.append([x, y, prefab])

    def changeSize(self, c, d):
        #c is change (whether adding or subtracting a row)
        #d is constant determining the direction of change
        if d != DOWN and d != UP:
            self.x += c
            if d == LEFT or d == UP_LEFT or d == DOWN_LEFT:
            #TODO: add something here that shifts all prefabs in grid over by 1 to the RIGHT
                pass
        if d != LEFT and d != RIGHT:
            self.y += c
            if d == DOWN or d == DOWN_RIGHT or d == DOWN_LEFT:
            #Same TODO as above except shift by 1 DOWN
                pass

        self.repaint()
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.rband:
                self.origin = e.pos()
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()

    def mouseMoveEvent(self, e):
        if self.rband:
            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, e.pos()).normalized())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.rband:
                print(QRect(self.origin, e.pos()))
                self.rubberBand.hide()
                
class GridSquare(QRect):
    def __init__(self, x, y, w, h):
        super(GridSquare, self).__init__(x, y, w, h)
        self.x = x
        self.y = y
        
class GridWidgetContainer(QWidget):
    def __init__(self, grid_widget):
        super(GridWidgetContainer, self).__init__()
        #self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        arrow = QPixmap("icons/arrow.png") #initial image is facing up
        arrows = []
        self.inner = QGridLayout()
        self.outer = QGridLayout()
        locs = [(0,1),
                (0,2),
                (1,2),
                (2,2),
                (2,1),
                (2,0),
                (1,0),
                (0,0)]
        for rot in range(len(locs)):
            transform = QTransform().rotate(45*rot)
            icon = arrow.transformed(transform, Qt.SmoothTransformation)
            arrows.append(ExpandButton(icon, rot, grid_widget))

        for i, loc in enumerate(locs):
            self.inner.addWidget(arrows[i], loc[0], loc[1])
        self.inner.addWidget(grid_widget, 1, 1)

        self.outer.addLayout(self.inner, 1, 1)
        self.outer.setColumnStretch(0, 1)
        self.outer.setColumnStretch(2, 1)
        self.outer.setRowStretch(0, 1)
        self.outer.setRowStretch(2, 1)

        self.setLayout(self.outer)

        
UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT = 0, 1, 2, 3, 4, 5, 6, 7
class ExpandButton(QPushButton):
    def __init__(self, icon, num, grid_widget):
        super(ExpandButton, self).__init__()
        self.id = num
        self.setIcon(QIcon(icon))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clicked.connect(lambda: grid_widget.changeSize(1, self.id))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda: grid_widget.changeSize(-1, self.id))        

##class DragArrow(QLabel):
##    def __init__(self, rot, grid_widget):
##        super(DragArrow, self).__init__()
##        self.grid_widget = grid_widget
##        self.start_drag = None
##        self.drag_x = 0
##        self.drag_y = 0
##        self.orientation = rot
##        if self.orientation == UP or self.orientation == DOWN:
##            self.setCursor(Qt.SizeVerCursor)
##        elif self.orientation == UP_RIGHT or self.orientation == DOWN_LEFT:
##            self.setCursor(Qt.SizeBDiagCursor)
##        elif self.orientation == RIGHT or self.orientation == LEFT:
##            self.setCursor(Qt.SizeHorCursor)
##        elif self.orientation == DOWN_RIGHT or self.orientation == UP_LEFT:
##            self.setCursor(Qt.SizeFDiagCursor)
##        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
##
##    def mousePressEvent(self, e):
##        self.start_drag = e.pos()
##
##    def mouseMoveEvent(self, e):
##        if self.orientation == RIGHT or self.orientation == UP_RIGHT or self.orientation == DOWN_RIGHT:
##            x_dir = 1
##        elif self.orientation == LEFT or self.orientation == UP_LEFT or self.orientation == DOWN_LEFT:
##            x_dir = -1
##        else:
##            x_dir = 0
##        
##        if self.orientation == UP or self.orientation == UP_RIGHT or self.orientation == UP_LEFT:
##            y_dir = 1
##        elif self.orientation == DOWN or self.orientation == DOWN_RIGHT or self.orientation == DOWN_LEFT:
##            y_dir = -1
##        else:
##            y_dir = 0
##            
##        d = e.pos() - self.start_drag #difference btw two points
##        qx = d.x() / (self.grid_widget.spacing + self.grid_widget.grid_width) #quotient btw d and one grid row
##        qy = d.y() / (self.grid_widget.spacing + self.grid_widget.grid_width)
##        if int(qx) != 0: #try math.round() instead of int here
##            #print(self.drag_x)
##            self.grid_widget.changeX(int(qx), x_dir)
##            #self.drag_x = int(qx)
##        if int(qy) != self.drag_y: #try math.round() instead of int here
##            self.grid_widget.changeY(int(qy) - self.drag_y, y_dir)
##            self.drag_y = int(qy)
##
##    def mouseReleaseEvent(self, e):
##        self.drag_x = 0
##        self.drag_y = 0
##        self.start_drag = None
        

def main():
    app = QApplication(sys.argv)
    grid = GridWidget(20,20)
    container = GridWidgetContainer(grid)
    container.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
