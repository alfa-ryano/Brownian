import sys
from PyQt4 import QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as pltPrice
import matplotlib.pyplot as pltDelta
import matplotlib.animation as animationPrice
import matplotlib.animation as animationDelta
from matplotlib.figure import Figure
import numpy as np

class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.animationPrice = None
        self.animationDelta = None

        uic.loadUi('Main.ui', self)
        self.buttonApply.clicked.connect(self.on_push_button_buy_clicked)
        self.buttonStart.clicked.connect(self.on_push_button_start_clicked)

        self.figurePrice = pltPrice.figure()
        self.canvasPrice = FigureCanvas(self.figurePrice)
        self.layoutGraphPrice.addWidget(self.canvasPrice)
        pltPrice.xlim(0, 100)
        pltPrice.ylim(0, 45)
        pltPrice.xlabel('time')
        pltPrice.title('price')
        pltPrice.grid()

        self.figureDelta = pltDelta.figure()
        self.canvasDelta = FigureCanvas(self.figureDelta)
        self.layoutGraphDelta.addWidget(self.canvasDelta)
        pltDelta.xlim(0, 100)
        pltDelta.ylim(0, 45)
        pltDelta.xlabel('time')
        pltDelta.title('price')
        pltDelta.grid()

        print "AAA"

    def on_push_button_start_clicked(self):

        if self.animationPrice != None:
            self.animationPrice.event_source.stop()
        self.canvasPrice.figure.clear()
        self.layoutGraphPrice.removeWidget(self.canvasPrice)
        self.canvasPrice.deleteLater()
        self.canvasPrice = None

        self.figurePrice = pltPrice.figure()
        self.canvasPrice = FigureCanvas(self.figurePrice)
        self.layoutGraphPrice.addWidget(self.canvasPrice)
        self.plotPrice()

        if self.animationDelta != None:
            self.animationDelta.event_source.stop()
        self.canvasDelta.figure.clear()
        self.layoutGraphDelta.removeWidget(self.canvasDelta)
        self.canvasDelta.deleteLater()
        self.canvasDelta = None

        self.figureDelta = pltDelta.figure()
        self.canvasDelta = FigureCanvas(self.figureDelta)
        self.layoutGraphDelta.addWidget(self.canvasDelta)
        self.plotDelta()


        print "BBB"

    def on_push_button_buy_clicked(self):
        print "AAAAA"

    def plotPrice(self):
        def update_line(num, data, line):
            line.set_data(data[..., :num])
            return line,

        T = 100
        mu = 0.0
        sigma = 0.1
        S0 = 20
        dt = 0.1
        N = round(T / dt)
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
        X = (mu - 0.5 * sigma ** 2) * t + sigma * W
        S = S0 * np.exp(X)
        x = np.array([t, S])

        data = x
        l, = pltDelta.plot([], [])
        pltPrice.xlim(0, 100)
        pltPrice.ylim(0, 45)
        pltPrice.xlabel('time')
        pltPrice.title('price/unit')
        pltPrice.grid()

        self.animationPrice = animationPrice.FuncAnimation(self.figurePrice, update_line, 1000, fargs=(data, l),
                                                           interval=20, blit=False, repeat=False)
        self.canvasPrice.draw()
        self.canvasPrice.show()

    def plotDelta(self):
        def update_line(num, data, line):
            line.set_data(data[..., :num])
            return line,

        T = 100
        mu = 0.0
        sigma = 0.1
        S0 = 20
        dt = 0.1
        N = round(T / dt)
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
        X = (mu - 0.5 * sigma ** 2) * t + sigma * W
        S = S0 * np.exp(X)
        x = np.array([t, S])

        data = x
        l, = pltDelta.plot([], [])
        pltDelta.xlim(0, 100)
        pltDelta.ylim(0, 45)
        pltDelta.xlabel('time')
        pltDelta.title('delta')
        pltDelta.grid()

        self.animationDelta = animationDelta.FuncAnimation(self.figureDelta, update_line, 1000, fargs=(data, l),
                                                           interval=20, blit=False, repeat=False)

        self.canvasDelta.draw()
        self.canvasDelta.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())