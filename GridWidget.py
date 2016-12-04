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
        self.draw_list = [] #draw_list contains list of icons and where to draw them
        #self.prefab_list = [] #prefab_list contains the list of prefabs and where they are located
        self.cur_prefab = None
        self.polys = []
        self.polys_color = []
        #self.startX = 0
        #self.startY = 0
        #self.setMouseTracking(True)
        self.scale = 64
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
        
        for x in range(self.spacing, self.x*self.grid_width, self.grid_width):
            x += self.spacing*x/self.grid_width
            for y in range(self.spacing, self.y*self.grid_width, self.grid_width):
                y += self.spacing*y/self.grid_width
                self.grid_list.append(GridSquare(x, y, self.grid_width, self.grid_width))
                qp.drawRect(self.grid_list[-1])

        w = self.x*self.spacing + self.x*self.grid_width
        h = self.y*self.spacing + self.y*self.grid_width
        self.setFixedSize(QSize(w, h))
        
        ##Draw the Prefabs
        qp.setPen(QColor(255, 0, 0, 255))
        self.polys = []
        for prefab in self.draw_list:
            for poly in prefab[2]:
                points = []
                for p in poly:
                    points.append([c/self.scale*(self.spacing+self.grid_width) for c in p])
                self.polys.append(QPolygon([QPoint(prefab[X]*(self.spacing+self.grid_width) + points[p][X], prefab[Y]*(self.spacing+self.grid_width) + points[p][Y]) for p in range(len(points))]))
        for i, p in enumerate(self.polys):
            qp.setBrush(QBrush(self.polys_color[i]))
            qp.drawPolygon(p)
            
    def appendPrefabs(self, x, y, prefab):
        #prefab is a list of the points in its icon
        self.draw_list.append([x, y, prefab])

##    def updateDrawList(self, draw_list):
##        self.draw_list = draw_list
##        self.polys_color = [None for i in draw_list]
##        self.repaint()

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
        elif e.button() == Qt.LeftButton:
            p = self.closestP(e)
            self.draw_list.append([p.x(), p.y(), self.cur_prefab.draw_list])
            self.polys_color.append(self.cur_prefab.color_list)

    def mouseMoveEvent(self, e):
        if self.rband:
            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, e.pos()).normalized())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.rband:
                print(QRect(self.origin, e.pos()))
                self.rubberBand.hide()

    def closestP(self, e):
        e.pos()

    def updatePrefab(self, prefab):
        self.cur_prefab = prefab

class CreatePrefabGridWidget(GridWidget):
    #in createPrefab, put a widget at the side to control the size of bounding box
    def __init__(self, x, y, rband=False):
        super(CreatePrefabGridWidget, self).__init__(x, y, rband)
        self.cur_color = None #color as defined by the color picker in CreatePrefab
        self.cur_poly = None #index of the current polygon mouse is hovering over
        self.setMouseTracking(True)
        
    def mousePressEvent(self, e):
        if self.cur_poly != None:
            if e.button() == Qt.LeftButton:
                self.polys_color[self.cur_poly] = self.cur_color
            elif e.button() == Qt.RightButton:
                self.polys_color[self.cur_poly] = None
            self.repaint()

    def mouseMoveEvent(self, e):
        for i, poly in enumerate(reversed(self.polys)):
            if poly.containsPoint(e.pos(), Qt.OddEvenFill):
                self.cur_poly = len(self.polys) - 1 - i
                self.setCursor(Qt.PointingHandCursor)
                return
        self.cur_poly = None
        self.setCursor(Qt.ArrowCursor)

    def updateDrawList(self, draw_list):
        self.draw_list = [[0, 0, draw_list]]
        self.polys_color = [None for i in draw_list]
        self.repaint()

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
##
##    def mouseMoveEvent(self, e):
##        if self.id == UP or self.id == UP_RIGHT or self.id == UP_LEFT:
##            self.y = e.y()
##        elif self.id == DOWN or self.id == DOWN_RIGHT or self.id == DOWN_LEFT:
##            self.y = e.y()
##
##        if self.id == RIGHT or self.id == UP_RIGHT or self.id == DOWN_RIGHT:
##            self.x = e.x()
##        elif self.id == LEFT or self.id == UP_LEFT or self.id == DOWN_LEFT:
##            self.x = e.x()

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
    import pickle
    import pf
    
    app = QApplication(sys.argv)
    grid = GridWidget(20,20)
    container = GridWidgetContainer(grid)
    container.show()

    tile_list1 = QListWidget()
    tile_list2 = QListWidget()
    tile_list3 = QListWidget()
    tab_dict = {"Geometry":tile_list1, "Map Layout":tile_list2, "Fun/Other":tile_list3}

    with open("tf2/prefabs.dat", "rb") as f:
        prefab_list = pickle.load(f)

    for p in prefab_list:
        prefab = pf.Prefab(p)
        tab_dict[prefab.section].addItem(prefab.text)

    list_tab_widget = QTabWidget()
    list_tab_widget.addTab(tile_list1,'Geometry')
    list_tab_widget.addTab(tile_list2,'Map Layout')
    list_tab_widget.addTab(tile_list3,'Fun/Other')

    prefab_dock = QDockWidget("Prefabs")
    prefab_dock.setWidget(list_tab_widget)
    prefab_dock.setFloating(True)
    prefab_dock.show()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
