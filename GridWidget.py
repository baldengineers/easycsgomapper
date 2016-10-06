import sys
from PySide.QtCore import *
from PySide.QtGui import *
import main

class GridWidget(QWidget):
    def __init__(self, spacing=25):
        super(GridWidget, self).__init__()
        self.spacing = spacing
        self.scale_list = [32,64,128,256,512]
        self.scale = self.scale_list[1]
        self.pList = []
        self.setCursor(Qt.CrossCursor)

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

        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_BracketLeft:
            self.changeScale(-1)
            self.repaint()
        elif e.key() == Qt.Key_BracketRight:
            self.changeScale(1)
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
        pen = QPen(Qt.lightGray, 1)
        qp.setPen(pen)

        scale_ind = 2 ** (self.scale_list.index(self.scale))
        
        coors = []
        for x in range(int(w/self.spacing)+1):
            pen.setColor(Qt.darkGray if (x/scale_ind).is_integer() else Qt.lightGray)
            qp.setPen(pen)
            x *= self.spacing
            line = QLineF(x,0.0,x,h)
            qp.drawLine(line)
            
            for y in range(int(h/self.spacing)+1):
                pen.setColor(Qt.darkGray if (y/scale_ind).is_integer() else Qt.lightGray)
                qp.setPen(pen)
                y *= self.spacing
                line = QLineF(x,y,x+self.spacing,y)
                qp.drawLine(line)
                coors.append([x,y])

        self.pList = []
        for c in coors:
            p = QPoint(c[0],c[1])
            self.pList.append(p)

    def setSpacing(self, spacing):
        self.spacing = spacing

    def changeSpacing(self, spacing):
        self.spacing += spacing

    def setScale(self, scale):
        self.scale = scale if scale in scale_list else self.scale #to make sure scale is not changed to anything other than those in scale_list

    def changeScale(self, change):
        cur_ind = self.scale_list.index(self.scale)
        self.scale = self.scale_list[cur_ind+change] if self.scale_list[0] != self.scale and change < 0 or self.scale_list[-1] != self.scale and change > 0 else self.scale

    def closestP(self, e):
        #finds the closest point to the mouse cursor(e)
        dist = []
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

        if e.button() == Qt.RightButton:
            self.origin = self.closestP(e)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
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

class CreatePrefabGridWidget(GridWidget):
    def __init__(self, spacing=25, parent=None):
        super(CreatePrefabGridWidget, self).__init__(spacing)
        self.parent = parent

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        self.update_icon(qp)
        qp.end()

    def update_icon(self, qp):
        #creates the polygons in poly list on the grid so user can color their prefab icon
        pen = QPen(Qt.gray, 5)
        qp.setPen(pen)

        X,Y,Z = 0,1,2
        rects = []
        for poly in [[[0, -448, 64], [512, -448, 64], [512, -512, 64]], [[0, -512, 0], [512, -512, 0], [512, -448, 0]], [[0, 0, 64], [64, 0, 64], [64, -448, 64]], [[0, -448, 0], [64, -448, 0], [64, 0, 0]], [[448, 0, 64], [512, 0, 64], [512, -448, 64]], [[448, -448, 0], [512, -448, 0], [512, 0, 0]], [[512, 0, 64], [960, 0, 64], [960, -64, 64]], [[512, -64, 0], [960, -64, 0], [960, 0, 0]], [[512, -448, 64], [960, -448, 64], [960, -512, 64]], [[512, -512, 0], [960, -512, 0], [960, -448, 0]], [[896, -512, 64], [960, -512, 64], [960, -960, 64]], [[896, -960, 0], [960, -960, 0], [960, -512, 0]], [[0, -896, 64], [448, -896, 64], [448, -960, 64]], [[0, -960, 0], [448, -960, 0], [448, -896, 0]], [[448, -512, 64], [512, -512, 64], [512, -960, 64]], [[448, -960, 0], [512, -960, 0], [512, -512, 0]]]:#self.parent.draw_list:
            points = []
            for p in poly:
                points.append([c/self.scale_list[0]*self.spacing for c in p])
            
            rects.append(QRect(QPoint(points[0][X], abs(points[0][Y])), QPoint(points[2][X], abs(points[2][Y]))))

        #might want to rewrite the following code:
##        for r1 in rects:
##            for r2 in rects:
##                draw = False
##                if r1 != r2:
##                    if r1.contains(r2):
##                        if points[rects.index(r1)][Z] > points[rects.index(r2)][Z]: #if r1 is higher on z axis than r2
##                            points.pop(rects.index(r2))
##                            rects.remove(r2)

        for r in rects:
            qp.drawRect(r) #in future, try to make this drawPolygon() and have a way to detect how many points the face has 

    def rect_contains(r1, r2):
        #checks if rectangle r2 is in rectangle r1
        pass

def main():
    app = QApplication(sys.argv)
    grid = CreatePrefabGridWidget()
    grid.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
