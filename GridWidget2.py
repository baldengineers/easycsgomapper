import sys
from PySide.QtCore import *
from PySide.QtGui import *

class GridWidget(QWidget):
    def __init__(self, x, y):
        super(GridWidget, self).__init__()
        self.x = x
        self.y = y
        self.spacing = 2
        self.grid_width = 16

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
        qp.setPen(QColor(0, 0, 0, 0))
        qp.setBrush(QColor(200, 200, 200, 200))
        
        for x in range(0, self.x*self.grid_width, self.grid_width):
            x += self.spacing*x/self.grid_width
            for y in range(0, self.y*self.grid_width, self.grid_width):
                y += self.spacing*y/self.grid_width
                qp.drawRect(x, y, self.grid_width, self.grid_width)

        w = self.x*self.spacing + self.x*self.grid_width
        h = self.y*self.spacing + self.y*self.grid_width
        self.setFixedSize(QSize(w, h))

    def changeX(self, c, d):
        #c is the change
        #d is the direction of change: 1 is right, -1 is left
        self.x += c
        #TODO: add directional code here
        self.repaint()

    def changeY(self, c, d):
        #c is the change
        #d is the direction of change: 1 is up, -1 is down
        self.y += c
        #TODO: add directional code here
        self.repaint()

class GridLayout(QGridLayout):
    def __init__(self, grid_widget):
        super(GridLayout, self).__init__()
        arrow = QPixmap("icons/arrow.png") #initial image is facing up
        btns = []
        for rot in range(4):
            transform = QTransform().rotate(90*rot)
            icon = arrow.transformed(transform, Qt.SmoothTransformation)
            btns.append(QPushButton())
            btns[-1].setIcon(QIcon(icon))

##        for i in range(len(btns)):
##            btns[i].setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))

        self.setRowMinimumHeight(1,50)
        self.addWidget(btns[0], 0, 1)
        btns[0].clicked.connect(lambda: grid_widget.changeY(1, 1))
        self.addWidget(btns[1], 1, 2)
        btns[1].clicked.connect(lambda: grid_widget.changeX(1, 1))
        self.addWidget(btns[2], 2, 1)
        btns[2].clicked.connect(lambda: grid_widget.changeY(1, -1))
        self.addWidget(btns[3], 1, 0)
        btns[3].clicked.connect(lambda: grid_widget.changeX(1, -1))
        self.addWidget(grid_widget, 1, 1)
        

def main():
    app = QApplication(sys.argv)
    grid = GridWidget(20,20)
    layout = GridLayout(grid)
    widget = QWidget()
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
