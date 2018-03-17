import sys
from PyQt4 import QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import numpy as np

class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.line_ani_1 = None
        self.line_ani_2 = None

        uic.loadUi('Main.ui', self)
        self.pushButtonBuy.clicked.connect(self.on_push_button_buy_clicked)
        self.pushButtonStart.clicked.connect(self.on_push_button_start_clicked)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas)

        print "AAA"

    def on_push_button_start_clicked(self):
        if self.line_ani_1 != None:
            self.line_ani_1.event_source.stop()
        if self.line_ani_2 != None:
            self.line_ani_2.event_source.stop()

        self.canvas.figure.clear()

        self.plota()
        self.plotb()
        print "BBB"

    def on_push_button_buy_clicked(self):
        print "AAAAA"

    def plota(self):
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
        l, = plt.plot([], [])
        plt.xlim(0, 100)
        plt.ylim(0, 45)
        plt.xlabel('time')
        plt.title('price')
        plt.grid()

        self.line_ani_1 = animation.FuncAnimation(self.figure, update_line, 1000, fargs=(data, l),
                                                  interval=20, blit=False, repeat=False)
        self.canvas.draw()
        self.canvas.show()

    def plotb(self):
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
        l, = plt.plot([], [])
        plt.xlim(0, 100)
        plt.ylim(0, 45)
        plt.xlabel('time')
        plt.title('price')
        plt.grid()

        self.line_ani_2 = animation.FuncAnimation(self.figure, update_line, 1000, fargs=(data, l),
                                                  interval=20, blit=False, repeat=False)
        self.canvas.draw()
        self.canvas.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())