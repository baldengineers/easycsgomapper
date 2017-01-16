import sys
import math
import itertools
import geo
from pf import Prefab
from PySide.QtCore import *
from PySide.QtGui import *

X,Y = 0,1

class GridWidget(QGraphicsView):
    overlapped = Signal(bool)
    prefab_outline = QPen(QColor(0, 0, 0, 255))
    spacing = 2
    grid_width = 16
    def __init__(self, x, y, parent=None):
        super(GridWidget, self).__init__()
        self.setMouseTracking(True)
        self.parent = parent
##        self.x = x
##        self.y = y
        self.p_list = []
        self.draw_list = [] #draw_list contains list of icons and where to draw them
        self.cur_prefab = None
        
        self.overlapping = False #if prefabs are overlapping
        self.prefabs = []
        #self.startX = 0
        #self.startY = 0
        self.prefab_scale = 64
        self.grid_list = []
        #vars for rubber band
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        #set up graphics
        self.scene = QGraphicsScene(self)
        self.setSize(x,y)
        self.setScene(self.scene)
        #set up different modes
        self.add_mode = False
        self.select_mode = False
        self.move_mode = False

##    def paintEvent(self, e):
##        qp = QPainter()
##        qp.begin(self)
##        self.draw(qp)
##        qp.end()

    def setSize(self, x, y):
        self.x = x
        self.y = y
        w = self.x*GridWidget.spacing + self.x*GridWidget.grid_width
        h = self.y*GridWidget.spacing + self.y*GridWidget.grid_width
        self.scene.setSceneRect(0, 0, w, h)

        ##Draw Grid
        pen = QPen(QColor(0, 0, 0, 0))
        brush = QBrush(QColor(200, 200, 200, 200) if not self.overlapping else QColor(200, 100, 100, 200))
        for ix, x in enumerate(range(GridWidget.spacing, w, GridWidget.grid_width)):
            x += GridWidget.spacing*x/GridWidget.grid_width
            for iy, y in enumerate(range(GridWidget.spacing, h, GridWidget.grid_width)):
                y += GridWidget.spacing*y/GridWidget.grid_width
                self.grid_list.append(GridSquare(x, y, GridWidget.grid_width, GridWidget.grid_width, pen, brush))
                self.p_list.append(QPoint(x-GridWidget.spacing/2,y-GridWidget.spacing/2)) #subtract GridWidget.spacing to center prefab over boxes
                self.scene.addItem(self.grid_list[-1])

        ##Draw the Prefabs
        pen = GridWidget.prefab_outline
        polys = []
        for x, prefab in enumerate(self.draw_list):
            for y, poly in enumerate(prefab[2]):
                points = []
                for p in poly:
                    points.append([c/self.prefab_scale*(GridWidget.spacing+GridWidget.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
                brush = QBrush(prefab.color_list[i])
                polys.append(PrefabPoly([QPoint(x + points[p][X], y + points[p][Y]) for p in range(len(points))], pen, brush, self))
                self.scene.addItem(polys[-1])

    def placePrefab(self, x, y, prefab):
        #self.prefabs.append(PrefabItem(x, y, prefab.draw_list, prefab.color_list, self))
        polys = []
        pen = GridWidget.prefab_outline
        for i, poly in enumerate(prefab.draw_list):
            points = []
            for p in poly:
                points.append([c/self.prefab_scale*(GridWidget.spacing+GridWidget.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
            brush = QBrush(prefab.color_list[i])
            polys.append(PrefabPoly([QPoint(x + points[p][X], y + points[p][Y]) for p in range(len(points))], pen, brush, self))
            self.scene.addItem(polys[-1])

        if not isinstance(self, CreatePrefabGridWidget):
            PrefabItemGroup.setAllCursor(Qt.CrossCursor)
            self.prefabs.append(PrefabItemGroup(x, y, prefab, self))
            for p in polys:
                self.prefabs[-1].addToGroup(p)
            self.scene.addItem(self.prefabs[-1])
            
##    def draw(self, qp):
##        size = self.size()
##        w = size.width()
##        h = size.height()
        
##        qp.setPen(QColor(0, 0, 0, 0))
##        qp.setBrush(QColor(200, 200, 200, 200) if not self.overlapping else QColor(200, 100, 100, 200))
##        
##        for x in range(GridWidget.spacing, self.x*GridWidget.grid_width, GridWidget.grid_width):
##            x += GridWidget.spacing*x/GridWidget.grid_width
##            for y in range(GridWidget.spacing, self.y*GridWidget.grid_width, GridWidget.grid_width):
##                y += GridWidget.spacing*y/GridWidget.grid_width
##                self.grid_list.append(GridSquare(x, y, GridWidget.grid_width, GridWidget.grid_width))
##                self.p_list.append(QPoint(x-GridWidget.spacing,y-GridWidget.spacing)) #subtract GridWidget.spacing to center prefab over boxes
##                qp.drawRect(self.grid_list[-1])
##
##        w = self.x*GridWidget.spacing + self.x*GridWidget.grid_width
##        h = self.y*GridWidget.spacing + self.y*GridWidget.grid_width
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
##                    points.append([c/self.prefab_scale*(GridWidget.spacing+GridWidget.grid_width) for c in p]) #scales the points of the prefabs down to the current scale of gridwidget
##                self.polys.append(PrefabPoly([QPoint(prefab[X] + points[p][X], prefab[Y] + points[p][Y]) for p in range(len(points))]))
##                qp.setBrush(QBrush(prefab[3][y]))
##                qp.drawPolygon(self.polys[-1])
##
##        for i1, poly1 in enumerate(self.polys):
##            for i2, poly2 in enumerate(self.polys):
##                if i1 != i2:
##                    if poly1.intersected(poly2):
##                        self.overlapping = True
##                        break
##                    elif self.overlapping:
##                        self.overlapping = False
##            if self.overlapping:
##                break
##
##        if self.overlapping:
##            self.overlapped.emit(True)
##        else:
##            self.overlapped.emit(False)

    def changeSize(self, c, d):
        #c is change (whether adding or subtracting a row)
        #d is constant determining the direction of change
        if d != DOWN and d != UP:
            self.x += c
            if d == LEFT or d == UP_LEFT or d == DOWN_LEFT:
                for prefab in self.draw_list:
                    prefab[X] += c*(GridWidget.spacing+GridWidget.grid_width)
        if d != LEFT and d != RIGHT:
            self.y += c
            if d == UP or d == UP_LEFT or d == UP_RIGHT:
                for prefab in self.draw_list:
                    prefab[Y] += c*(GridWidget.spacing+GridWidget.grid_width)

        self.repaint()
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def enableAddPrefab(self, add):
        if add:
            self.viewport().setCursor(Qt.CrossCursor)
            PrefabItemGroup.setAllCursor(Qt.CrossCursor)            
            self.add_mode = True
        else:
            self.add_mode = False

    def enableSelect(self, select):
        #this function is called when the toggle state of self.parent.select_action changes in main.py
        if select:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            self.viewport().setCursor(Qt.ArrowCursor)
            PrefabItemGroup.setAllCursor(Qt.SizeAllCursor)
            PrefabItemGroup.setAllSelectable(True)
            PrefabItemGroup.setAllMovable(True)
            self.select_mode = True
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            PrefabItemGroup.setAllSelectable(False)
            PrefabItemGroup.setAllMovable(False)
            self.select_mode = False

    def mousePressEvent(self, e):        
        if e.button() == Qt.LeftButton:
            if self.add_mode:
                p = self.closestP(e)
                self.placePrefab(p.x(), p.y(), self.cur_prefab)

        QGraphicsView.mousePressEvent(self, e)

    def mouseMoveEvent(self, e):
        QGraphicsView.mouseMoveEvent(self, e)

    def mouseReleaseEvent(self, e):
        QGraphicsView.mouseReleaseEvent(self, e)
        
        for p in self.prefabs:
            for c in p.childItems():
                for i in self.scene.collidingItems(c):
                    if isinstance(i, PrefabPoly) and i.parentItem() != p:
##                        polygon = c.polygon().intersected(i.polygon()).toPolygon()
##                        print(polygon)
##                        for p in polygon:
##                            print(p)
##                        print(geo.area([[p.x(), p.y()] for p in polygon]))
                        self.overlapping = True
                        self.overlapped.emit(True)
                        return
                    elif self.overlapping:
                        self.overlapping = False

        self.overlapped.emit(False)

    def wheelEvent(self, e):
        factor = 1.41 ** (e.delta()/240.0)
        self.scale(factor, factor)

    def closestP(self, e, m=True):
        #finds the closest point to the mouse cursor/QPoint (e)
        #m is whether or not to map to scene
        if m:
            e = self.mapToScene(e.pos())
        dist = []
        for p in self.p_list:
            dist.append([abs(e.x() - p.x()),abs(e.y() - p.y())])
        xy = min(d for d in dist)
        return self.p_list[dist.index(xy)]

    def updatePrefab(self, prefab):
        self.cur_prefab = prefab

class CreatePrefabGridWidget(GridWidget):
    #in createPrefab, put a widget at the side to control the size of bounding box
    def __init__(self, x, y):
        super(CreatePrefabGridWidget, self).__init__(x, y)
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
        PrefabPoly.setAllCursor(Qt.PointingHandCursor)
        
class GridSquare(QGraphicsRectItem):
    #this class is used to facilitate exporting maps
    def __init__(self, x, y, w, h, pen, brush):
        super(GridSquare, self).__init__(x, y, w, h)
        self.posx = x
        self.posy = y
        self.setEnabled(False)
        self.setPen(pen)
        self.setBrush(brush)

class PrefabPoly(QGraphicsPolygonItem):
    #these are the individuo polygons in each prefab
    #http://stackoverflow.com/questions/26315584/apply-a-function-to-all-instances-of-a-class

    objs = [] #contains all the instances of the class
    
    def __init__(self, points, pen, brush, parent):
        super(PrefabPoly, self).__init__(QPolygon(points))
        self.setPen(pen)
        self.setBrush(brush)
        self.parent = parent
        PrefabPoly.objs.append(self)
        
    def mousePressEvent(self, e):
        if isinstance(self.parent, CreatePrefabGridWidget):
            if e.button() == Qt.LeftButton:
                self.setBrush(self.parent.cur_color)
            else:
                self.setBrush(QBrush(None))

        QGraphicsPolygonItem.mousePressEvent(self, e)

    def itemChange(self,change,value):
        return QGraphicsItem.itemChange(self, change, value)

    @classmethod
    def setAllCursor(cls, cursor):
        for obj in cls.objs:
            obj.setCursor(cursor)

class PrefabItemGroup(QGraphicsItemGroup):
    #these are the individuo polygons in each prefab

    objs = []
    
    def __init__(self, x, y, prefab, parent):
        super(PrefabItemGroup, self).__init__()
        self.posx = int(x/(GridWidget.spacing+GridWidget.grid_width))
        self.posy = int(y/(GridWidget.spacing+GridWidget.grid_width))
        self.setX(x)
        self.setY(y)
        self.prefab = prefab
        self.parent = parent
        self.setFlag(QGraphicsItemGroup.ItemSendsGeometryChanges)
        PrefabItemGroup.objs.append(self)

    def mousePressEvent(self, e):
        QGraphicsItemGroup.mousePressEvent(self, e)

    def itemChange(self, change, value):
##        print(self.x())
##        print(self.y())
        self.posx = int(self.x()/(GridWidget.spacing+GridWidget.grid_width))
        self.posy = int(self.y()/(GridWidget.spacing+GridWidget.grid_width))
        if change == QGraphicsItemGroup.ItemPositionChange:
            new_pos = value.toPoint()
            cp = self.parent.closestP(QPoint(new_pos.x(), new_pos.y()), False) #False = do not map
            new_pos.setX(cp.x())
            new_pos.setY(cp.y())
            self.posx = int(cp.x()/(GridWidget.spacing+GridWidget.grid_width))
            self.posy = int(cp.y()/(GridWidget.spacing+GridWidget.grid_width))
            return new_pos
        return QGraphicsItemGroup.itemChange(self, change, value)

##    def boundingPoly(self):
##        #poly = list(k for k,_ in itertools.groupby(sorted([item for sublist in self.prefab.draw_list for item in sublist]))) #removes duplicate points in draw_list
##        #poly = geo.sortPtsClockwise(poly)
##        poly = [item for sublist in self.prefab.draw_list for item in sublist]
##        points = []
##        for p in poly:
##            points.append([c/self.parent.prefab_scale*(GridWidget.spacing+GridWidget.grid_width) for c in p])
##
##        return QPolygon([QPoint(self.x() + points[p][X], self.y() + points[p][Y]) for p in range(len(points))])
##        polygon = QPolygon()
##        for item in self.childItems():
##            poly = item.polygon().toPolygon()
##            for i in range(len(poly)):
##                poly.setPoint(i, QPoint(poly.point(i).x() + self.x(), poly.point(i).y() + self.y()))
##            polygon += poly
##            poly = polygon + item.polygon().toPolygon()
##            polygon = QPolygon(poly)
##        return polygon

    def shape(self):
        path = QPainterPath()
        for item in self.childItems():
            poly = item.mapToScene(item.polygon())
            path.addPolygon(poly)
            path.closeSubpath()
##        self.scene().addPath(path)
        return path

    @classmethod
    def setAllCursor(cls, cursor):
        for obj in cls.objs:
            obj.setCursor(cursor)

    @classmethod
    def setAllSelectable(cls, selectable):
        for obj in cls.objs:
            obj.setFlag(QGraphicsItemGroup.ItemIsSelectable, selectable)

    @classmethod
    def setAllMovable(cls, movable):
        for obj in cls.objs:
            obj.setFlag(QGraphicsItemGroup.ItemIsMovable, movable)
        
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
            self.overlapLabel.show()
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
