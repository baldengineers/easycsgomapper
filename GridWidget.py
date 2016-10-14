import sys
from PySide.QtCore import *
from PySide.QtGui import *
import main

class GridWidget(QWidget):
    def __init__(self, parent=None, spacing=25):
        super(GridWidget, self).__init__(parent)
        self.spacing = spacing
        self.scale_list = [32,64,128,256,512]
        self.scale = self.scale_list[1]
        self.pList = [] #intersection points of graph lines
        self.no_draw = 1 #when zoomed out, use no draw to stop drawing unnecessary lines
        self.setCursor(Qt.CrossCursor)

    def wheelEvent(self, e):
        e.accept()
        self.changeSpacing(e.delta()/40) #replace with scrollspeed constant

        if self.spacing < 16:
            self.no_draw = int(round(16/self.spacing)) + 1
        else:
            self.no_draw = 1

        print('spacing', self.spacing)
        print("no_draw ",self.no_draw)

        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_BracketLeft:
            e.accept()
            self.changeScale(-1)
            self.repaint()
        elif e.key() == Qt.Key_BracketRight:
            e.accept()
            self.changeScale(1)
            self.repaint()
        else:
            e.ignore()
        
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

        scale_ind = self.scaleSpacing()
        
        coors = []
        for x in range(int(w/self.spacing)+1):
##            pen.setColor(Qt.darkGray if (x/scale_ind).is_integer() else Qt.lightGray)
##            qp.setPen(pen)
            x *= self.spacing
            if (x/self.no_draw).is_integer():
                line = QLineF(x,0.0,x,h)
                qp.drawLine(line)
            
            for y in range(int(h/self.spacing)+1):
##                pen.setColor(Qt.darkGray if (y/scale_ind).is_integer() else Qt.lightGray)
##                qp.setPen(pen)
                y *= self.spacing
                if (y/self.no_draw).is_integer():
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
        self.spacing += spacing if self.spacing + spacing > 0 else 0

    def setScale(self, scale):
        self.scale = scale if scale in scale_list else self.scale #to make sure scale is not changed to anything other than those in scale_list

    def changeScale(self, change):
        cur_ind = self.scale_list.index(self.scale)
        self.scale = self.scale_list[cur_ind+change] if self.scale_list[0] != self.scale and change < 0 or self.scale_list[-1] != self.scale and change > 0 else self.scale

    def scaleSpacing(self):
        return 2 ** (self.scale_list.index(self.scale))

    def iconScaleSpacing(self):
        return self.spacing #add more

    def closestP(self, e):
        #finds the closest point to the mouse cursor(e)
        dist = []
        for p in self.pList:
            dist.append([abs(e.pos().x() - p.x()),abs(e.pos().y() - p.y())])
        xy = min(d for d in dist)
        return self.pList[dist.index(xy)]

class MainGridWidget(GridWidget):
    #This is the grid for the main program, where you place the prefabs
    def __init__(self, parent=None, spacing=25):
        #spacing controls how spaced out the lines are
        super(MainGridWidget, self).__init__(parent, spacing)
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
    def __init__(self, parent=None, spacing=25):
        super(CreatePrefabGridWidget, self).__init__(parent, spacing)
        self.draw_list = []
        w = 350; h = 350
        self.sizeHint = lambda: QSize(w, h)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        self.update_icon(qp)
        qp.end()

    def update_draw_list(self, draw_list):
        self.draw_list = draw_list
        self.repaint()

    def update_icon(self, qp):
        #creates the polygons in poly list on the grid so user can color their prefab icon
        pen = QPen(Qt.black, 3)
        qp.setPen(pen)

        X,Y,Z = 0,1,2
        polys = []
        for poly in self.draw_list:
            points = []
            for p in poly:
                points.append([c/self.scale_list[0]*self.spacing for c in p])
            polys.append(QPolygon([QPoint(points[i][X], points[i][Y]) for i in range(len(points))]))

        #might want to rewrite the following code:
##        for r1 in rects:
##            for r2 in rects:
##                draw = False
##                if r1 != r2:
##                    if r1.contains(r2):
##                        if points[rects.index(r1)][Z] > points[rects.index(r2)][Z]: #if r1 is higher on z axis than r2
##                            points.pop(rects.index(r2))
##                            rects.remove(r2)

        for p in polys:
            qp.drawPolygon(p)

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
        
