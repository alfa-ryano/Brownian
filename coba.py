import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class sliderdemo(QWidget):
    def __init__(self, parent=None):
        super(sliderdemo, self).__init__(parent)
        self.setMinimumHeight(200)
        self.setMinimumWidth(1000)
        layout = QVBoxLayout()
        self.l1 = QLabel("Hello")
        self.l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.l1)

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(20)
        self.sl.setTickPosition(QSlider.TicksBothSides)
        self.sl.setTickInterval(1)
        self.sl.setPageStep(0)

        layout.addWidget(self.sl)
        self.setLayout(layout)
        self.setWindowTitle("SpinBox demo")

        self.sl.valueChanged.connect(self.valuechange)
        self.sl.sliderMoved.connect(self.slidermoved)
        self.sl.sliderPressed.connect(self.sliderpressed)
        self.sl.sliderReleased.connect(self.sliderreleased)
        self.sl.mouseReleaseEvent = self.mousereleased

    def mousereleased(self, mouse_event):
        x = mouse_event.x()
        y = mouse_event.y()
        width = self.sl.width()
        unit = width / 100.25

        pos = round(x / unit)
        self.sl.setValue(pos)
        print pos


    def slidermoved(self):
        print "slider moved"

    def sliderpressed(self):
        print "slider pressed"

    def sliderreleased(self):
        print "slider released"

    def valuechange(self):
        print "value changed"
        size = self.sl.value()
        self.l1.setFont(QFont("Arial", size))


def main():
    app = QApplication(sys.argv)
    ex = sliderdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()