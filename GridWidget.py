import sys
import math
from pf import Prefab
from PySide.QtCore import *
from PySide.QtGui import *

X,Y = 0,1

class GridWidget(QGraphicsView):
    overlapped = Signal(bool)
    prefab_outline = QPen(QColor(0, 0, 0, 255))
    def __init__(self, x, y, rband=True):
        super(GridWidget, self).__init__()
        self.setMouseTracking(True)
##        self.x = x
##        self.y = y
        self.p_list = []
        self.draw_list = [] #draw_list contains list of icons and where to draw them
        #self.prefab_list = [] #prefab_list contains the list of prefabs and where they are located
        self.cur_prefab = None
        
        self.overlapping = False #if prefabs are overlapping
        self.prefabs = []
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
        #set up graphics
        self.scene = QGraphicsScene(self)
        self.setSize(x,y)
        self.setScene(self.scene)
        

        
        self.show()

##    def paintEvent(self, e):
##        qp = QPainter()
##        qp.begin(self)
##        self.draw(qp)
##        qp.end()

    def setSize(self, x, y):
        self.x = x
        self.y = y
        w = self.x*self.spacing + self.x*self.grid_width
        h = self.y*self.spacing + self.y*self.grid_width
        self.scene.setSceneRect(0, 0, w, h)

        ##Draw Grid
        pen = QPen(QColor(0, 0, 0, 0))
        brush = QBrush(QColor(200, 200, 200, 200) if not self.overlapping else QColor(200, 100, 100, 200))
        for x in range(self.spacing, w, self.grid_width):
            x += self.spacing*x/self.grid_width
            for y in range(self.spacing, h, self.grid_width):
                y += self.spacing*y/self.grid_width
                self.grid_list.append(GridSquare(x, y, self.grid_width, self.grid_width))
                self.p_list.append(QPoint(x-self.spacing,y-self.spacing)) #subtract self.spacing to center prefab over boxes
                self.scene.addRect(self.grid_list[-1], pen, brush)

        ##Draw the Prefabs
        pen = GridWidget.prefab_outline
        self.polys = []
        for x, prefab in enumerate(self.draw_list):
            for y, poly in enumerate(prefab[2]):
                points = []
                for p in poly:
                    points.append([c/self.scale*(self.spacing+self.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
                brush = QBrush(prefab.color_list[i])
                self.polys.append(PrefabPoly([QPoint(x + points[p][X], y + points[p][Y]) for p in range(len(points))], pen, brush, self))
                self.scene.addItem(self.polys[-1])

    def placePrefab(self, x, y, prefab):
        #self.prefabs.append(PrefabItem(x, y, prefab.draw_list, prefab.color_list, self))
        polys = []
        pen = GridWidget.prefab_outline
        for i, poly in enumerate(prefab.draw_list):
            points = []
            for p in poly:
                points.append([c/self.scale*(self.spacing+self.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
            brush = QBrush(prefab.color_list[i])
            polys.append(PrefabPoly([QPoint(x + points[p][X], y + points[p][Y]) for p in range(len(points))], pen, brush, self))
            self.scene.addItem(polys[-1])

        if not isinstance(self, CreatePrefabGridWidget):
            self.prefabs.append(PrefabItemGroup(x, y, prefab))
            for p in polys:
                self.prefabs[-1].addToGroup(p)
            self.scene.addItem(self.prefabs[-1])
        
        
##        pen = GridWidget.prefab_outline
##        
##        for i, poly in enumerate(prefab.draw_list):
##            points = []
##            for p in poly:
##                points.append([c/self.scale*(self.spacing+self.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
##            brush = QBrush(prefab.color_list[i])
##            self.polys.append(PrefabPoly([QPoint(x + points[p][X], y + points[p][Y]) for p in range(len(points))], pen, brush, self))
##            self.scene.addItem(self.polys[-1])
            

    def draw(self, qp):
##        size = self.size()
##        w = size.width()
##        h = size.height()
        
##        qp.setPen(QColor(0, 0, 0, 0))
##        qp.setBrush(QColor(200, 200, 200, 200) if not self.overlapping else QColor(200, 100, 100, 200))
##        
##        for x in range(self.spacing, self.x*self.grid_width, self.grid_width):
##            x += self.spacing*x/self.grid_width
##            for y in range(self.spacing, self.y*self.grid_width, self.grid_width):
##                y += self.spacing*y/self.grid_width
##                self.grid_list.append(GridSquare(x, y, self.grid_width, self.grid_width))
##                self.p_list.append(QPoint(x-self.spacing,y-self.spacing)) #subtract self.spacing to center prefab over boxes
##                qp.drawRect(self.grid_list[-1])
##
##        w = self.x*self.spacing + self.x*self.grid_width
##        h = self.y*self.spacing + self.y*self.grid_width
##        self.scene.setSceneRect(0, 0, w, h)
##        self.setFixedSize(w, h)
##        
##        ##Draw the Prefabs
##        qp.setPen(QColor(255, 0, 0, 255))
##        self.polys = []
##        for x, prefab in enumerate(self.draw_list):
##            for y, poly in enumerate(prefab[2]):
##                points = []
##                for p in poly:
##                    points.append([c/self.scale*(self.spacing+self.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
##                self.polys.append(PrefabPoly([QPoint(prefab[X] + points[p][X], prefab[Y] + points[p][Y]) for p in range(len(points))]))
##                qp.setBrush(QBrush(prefab[3][y]))
##                qp.drawPolygon(self.polys[-1])

        for i1, poly1 in enumerate(self.polys):
            for i2, poly2 in enumerate(self.polys):
                if i1 != i2:
                    if poly1.intersected(poly2):
                        self.overlapping = True
                        break
                    elif self.overlapping:
                        self.overlapping = False
            if self.overlapping:
                break

        if self.overlapping:
            self.overlapped.emit(True)
        else:
            self.overlapped.emit(False)

    def changeSize(self, c, d):
        #c is change (whether adding or subtracting a row)
        #d is constant determining the direction of change
        if d != DOWN and d != UP:
            self.x += c
            if d == LEFT or d == UP_LEFT or d == DOWN_LEFT:
                for prefab in self.draw_list:
                    prefab[X] += c*(self.spacing+self.grid_width)
        if d != LEFT and d != RIGHT:
            self.y += c
            if d == UP or d == UP_LEFT or d == UP_RIGHT:
                for prefab in self.draw_list:
                    prefab[Y] += c*(self.spacing+self.grid_width)

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
            self.placePrefab(p.x(), p.y(), self.cur_prefab)
            #self.draw_list.append([p.x(), p.y(), self.cur_prefab.draw_list, self.cur_prefab.color_list])
            #self.repaint()

        QGraphicsView.mousePressEvent(self, e)

    def mouseMoveEvent(self, e):
        if self.rband:
            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, e.pos()).normalized())

        QGraphicsView.mouseMoveEvent(self, e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.rband:
                print(QRect(self.origin, e.pos()))
                self.rubberBand.hide()

        QGraphicsView.mouseReleaseEvent(self, e)

    def closestP(self, e):
        #finds the closest point to the mouse cursor/QPoint (e)
        dist = []
        for p in self.p_list:
            dist.append([abs(e.x() - p.x()),abs(e.y() - p.y())])
        xy = min(d for d in dist)
        return self.p_list[dist.index(xy)]

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
                self.cur_prefab.color_list[self.cur_poly] = self.cur_color
            elif e.button() == Qt.RightButton:
                self.cur_prefab.color_list[self.cur_poly] = None
            self.updateColor()

        QGraphicsView.mousePressEvent(self, e)

    def updateColor(self):
        self.cur_prefab.draw_list[self.cur_poly]

    def updateDrawList(self, draw_list):
        self.cur_prefab = Prefab()
        self.cur_prefab.draw_list = draw_list
        self.cur_prefab.color_list = [None for i in draw_list]
        self.placePrefab(0, 0, self.cur_prefab)
        self.repaint()

class GridSquare(QRect):
    #this class is used to facilitate exporting maps
    def __init__(self, x, y, w, h):
        super(GridSquare, self).__init__(x, y, w, h)
        self.x = x
        self.y = y

class PrefabPoly(QGraphicsPolygonItem):
    #these are the individuo polygons in each prefab
    def __init__(self, points, pen, brush, parent):
        super(PrefabPoly, self).__init__(QPolygon(points))
        self.setPen(pen)
        self.setBrush(brush)
        self.setCursor(Qt.PointingHandCursor)
        self.parent = parent
        
    def mousePressEvent(self, e):
        if isinstance(self.parent, CreatePrefabGridWidget):
            if e.button() == Qt.LeftButton:
                self.setBrush(self.parent.cur_color)
            else:
                self.setBrush(QBrush(None))

        QGraphicsPolygonItem.mousePressEvent(self, e)

class PrefabItemGroup(QGraphicsItemGroup):
    #these are the individuo polygons in each prefab
    def __init__(self, x, y, prefab):
        super(PrefabItemGroup, self).__init__()
        self.x = x
        self.y = y
        self.prefab = prefab

##        for p in polys:
##            print("adding ", p, " to group")
##            self.addToGroup(p)
            
        #self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, e):
        QGraphicsItemGroup.mousePressEvent(self, e)
    
        
class GridWidgetContainer(QWidget):
    def __init__(self, grid_widget):
        super(GridWidgetContainer, self).__init__()
        self.grid_widget = grid_widget
        arrow = QPixmap("icons/arrow.png") #initial image is facing up
        arrows = []
        self.inner = QGridLayout()
        self.entire = QVBoxLayout()
        self.outer = QGridLayout()
        self.status = QStatusBar()
        self.overlapLabel = QLabel("Warning: Prefabs Overlapping!")
        grid_widget.overlapped.connect(self.displayStatus)
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
            arrows.append(ExpandButton(icon, rot, self.grid_widget))

        for i, loc in enumerate(locs):
            self.inner.addWidget(arrows[i], loc[X], loc[Y])
        self.inner.addWidget(self.grid_widget, 1, 1)

        self.entire.addLayout(self.inner)
        self.entire.addWidget(self.status)
        
        self.outer.addLayout(self.entire, 1, 1)
        self.outer.setColumnStretch(0, 1)
        self.outer.setColumnStretch(2, 1)
        self.outer.setRowStretch(0, 1)
        self.outer.setRowStretch(2, 1)

        self.setLayout(self.outer)

    def displayStatus(self, overlapped):
        if overlapped:
            self.status.addPermanentWidget(self.overlapLabel)
        else:
            self.status.removeWidget(self.overlapLabel)
        
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
