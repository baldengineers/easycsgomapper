import sys
from PySide.QtCore import *
from PySide.QtGui import *
import main
X,Y,Z = 0,1,2

#CURRENTLY, each grid line represents 32 hammer units

class GridWidget(QWidget):
    def __init__(self, parent=None, spacing=25, rband=True):
        super(GridWidget, self).__init__(parent)
        self.draw_list = []
        self.mouse_pos = None
        self.no_draw = 1 #when zoomed out, use no draw to stop drawing unnecessary lines
        self.no_draw_max = 16 #point at which no_draw starts to take effect
        self.pList = [] #intersection points of graph lines
        self.polys = []
        self.polys_color = []
        self.scale = 32
        self.scrollspeed = 2
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.spacing = spacing
        self.transform = [0,0]
        self.transform_origin = QPoint()
        self.transformspeed = self.scrollspeed * 10
        #vars for rubber band
        self.rband = rband #if rubberband is enabled
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def wheelEvent(self, e):
        self.changeSpacing(e.delta()/(20*self.scrollspeed)) #replace with scrollspeed constant
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Equal:
            self.changeSpacing(self.scrollspeed)
        elif e.key() == Qt.Key_Minus:
            self.changeSpacing(-self.scrollspeed)
        elif e.key() == Qt.Key_Space:
            self.transform = [0,0]
        elif e.key() == Qt.Key_Down:
            self.transform[Y] -= self.transformspeed
        elif e.key() == Qt.Key_Up:
            self.transform[Y] += self.transformspeed
        elif e.key() == Qt.Key_Right:
            self.transform[X] -= self.transformspeed
        elif e.key() == Qt.Key_Left:
            self.transform[X] += self.transformspeed

        self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.rband:
                self.origin = self.closestP(e.pos())
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()
        elif e.button() == Qt.LeftButton:
            #self.parent.cur_icon
            pass
        elif e.button() == Qt.MidButton:
            self.transform_origin = e.pos()
        
        self.mousePressCustom(e)
    
    def mousePressCustom(self, e):
        pass
    
    def mouseMoveEvent(self, e):
        self.mouse_pos = e.pos()
        if self.rband:
            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, self.closestP(e.pos())).normalized())
        if not self.transform_origin.isNull():
            self.transform[X] -= self.transform_origin.x() - e.pos().x()
            self.transform[Y] -= self.transform_origin.y() - e.pos().y()
            self.transform_origin = e.pos()
            self.repaint()
        
        self.mouseMoveCustom(e)

    def mouseMoveCustom(self, e):
        #custom reimplementation without disrupting original function
        pass
    
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            pass   
        #rubber band
        elif e.button() == Qt.RightButton:
            if self.rband:
                print(QRect(self.origin, self.closestP(e.pos())))
                self.rubberBand.hide()
        elif e.button() == Qt.MidButton:
            self.transform_origin = QPoint()
        
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        self.update_icon(qp)
        qp.end()

    def draw(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        #draw the gride.button() == Qt.LeftButton:
        pen = QPen(Qt.lightGray, 1)
        qp.setPen(pen)

        if self.spacing < self.no_draw_max:
            self.no_draw = int(round(self.no_draw_max/self.spacing)) + 1
        else:
            self.no_draw = 1

##        print('spacing',self.spacing)
##        print(self.no_draw)

        coords = [[],[]]
        start = [int(t % (self.spacing*self.no_draw)) for t in self.transform]
        
        for x in range(start[X], w, int(self.spacing*self.no_draw)):
            line = QLineF(x,0.0,x,h)
            qp.drawLine(line)
            coords[X].append(x)

        for y in range(start[Y], h, int(self.spacing*self.no_draw)):
            line = QLineF(0.0,y,w,y)
            qp.drawLine(line)
            coords[Y].append(y)

        self.pList = []
        for x in coords[X]:
            for y in coords[Y]:
                self.pList.append(QPoint(x,y))

    def update_icon(self, qp):
        #creates the polygons in poly list on the grid so user can color their prefab icon
        pen = QPen(Qt.black, 3)
        qp.setPen(pen)
  
        self.polys = []
        for poly in self.draw_list:
            points = []
            for p in poly:
                points.append([c/self.scale*self.spacing for c in p])
            self.polys.append(QPolygon([QPoint(points[p][X]+self.transform[X], points[p][Y]+self.transform[Y]) for p in range(len(points))]))

        for i, p in enumerate(self.polys):
            qp.setBrush(QBrush(self.polys_color[i]))
            qp.drawPolygon(p)

    def changeSpacing(self, spacing):
        self.spacing += spacing if self.spacing + spacing > 0 else -(self.spacing-1) #set to 0 if adding spacing makes it less than 0

    def closestP(self, pos):
        #finds the closest point to the mouse cursor/QPoint (pos)
        dist = []
        for p in self.pList:
            dist.append([abs(pos.x() - p.x()),abs(pos.y() - p.y())])
        xy = min(d for d in dist)
        return self.pList[dist.index(xy)]

class MainGridWidget(GridWidget):
    #This is the grid for the main program, where you place the prefabs
    def __init__(self, parent=None, spacing=25, rband=True):
        #spacing controls how spaced out the lines are
        super(MainGridWidget, self).__init__(parent, spacing, rband)
        #testing purposes
        self.cur_icon = [[[512, 512, 64], [512, 448, 64], [0, 448, 64], [0, 512, 64]], [[64, 448, 64], [64, 0, 64], [0, 0, 64], [0, 448, 64]], [[512, 448, 64], [512, 0, 64], [448, 0, 64], [448, 448, 64]], [[960, 64, 64], [960, 0, 64], [512, 0, 64], [512, 64, 64]], [[960, 512, 64], [960, 448, 64], [512, 448, 64], [512, 512, 64]], [[960, 960, 64], [960, 512, 64], [896, 512, 64], [896, 960, 64]], [[448, 960, 64], [448, 896, 64], [0, 896, 64], [0, 960, 64]], [[512, 960, 64], [512, 512, 64], [448, 512, 64], [448, 960, 64]]]
        self.cur_icon_color = [None for i in self.cur_icon]
        #self.cur_icon = None
        #self.cur_icon_color = None
        self.prefabs = [] #contains list of the prefabs in the grid, contains [icon,coordinate index for the point it is at(top left),moduleName(implement in main program)]
        self.setAcceptDrops(True)
        
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

    def mousePressCustom(self, e):
        if e.button() == Qt.LeftButton:
            pos = self.closestP(e.pos()) / self.spacing * self.scale
            for poly in self.cur_icon:
                print(self.transform)
                transform = [int(t/self.spacing*self.scale) for t in self.transform]
                self.draw_list.append([])
                for p in poly:
                    self.draw_list[-1].append([p[X] + transform[X] + pos.x(), p[Y] + transform[Y] + pos.y(), p[Z]])
            for c in self.cur_icon_color:
                self.polys_color.append(c)
            self.repaint()
        

class CreatePrefabGridWidget(GridWidget):
    def __init__(self, parent=None, spacing=25, rband=False):
        super(CreatePrefabGridWidget, self).__init__(parent, spacing, rband)
        #self.draw_list = [[[512, 512, 64], [512, 448, 64], [0, 448, 64], [0, 512, 64]], [[64, 448, 64], [64, 0, 64], [0, 0, 64], [0, 448, 64]], [[512, 448, 64], [512, 0, 64], [448, 0, 64], [448, 448, 64]], [[960, 64, 64], [960, 0, 64], [512, 0, 64], [512, 64, 64]], [[960, 512, 64], [960, 448, 64], [512, 448, 64], [512, 512, 64]], [[960, 960, 64], [960, 512, 64], [896, 512, 64], [896, 960, 64]], [[448, 960, 64], [448, 896, 64], [0, 896, 64], [0, 960, 64]], [[512, 960, 64], [512, 512, 64], [448, 512, 64], [448, 960, 64]]]
        w = 500
        h = 350
        self.sizeHint = lambda: QSize(w, h)
        self.cur_poly = [None, None] #the current polygon mouse is hovering over, with its index in self.polys
        self.cur_color = None
        
    def mousePressCustom(self, e):
        if self.cur_poly[0]:
            if self.cur_poly[0].containsPoint(e.pos(), Qt.OddEvenFill):
                if e.button() == Qt.LeftButton:
                    print(self.cur_color)
                    self.polys_color[self.cur_poly[1]] = self.cur_color
                elif e.button() == Qt.RightButton:
                    self.polys_color[self.cur_poly[1]] = None
                self.repaint()
                
    def mouseMoveCustom(self, e):
        for i, poly in enumerate(reversed(self.polys)):
            if poly.containsPoint(e.pos(), Qt.OddEvenFill):
                self.cur_poly = [poly, len(self.polys) - 1 - i]
                self.setCursor(Qt.PointingHandCursor)
                return
        self.cur_poly = [None, None]
        self.setCursor(Qt.CrossCursor)

    def update_draw_list(self, draw_list):
        self.draw_list = draw_list
        self.polys_color = [None for i in self.draw_list]
        self.repaint()

def main():
    app = QApplication(sys.argv)
    grid = MainGridWidget()
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
