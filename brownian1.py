from PyQt4 import QtGui, uic
from PyQt4.QtCore import QFile, QTextStream
from customutil import CountDownTimer
import matplotlib.pyplot as plot
import matplotlib.animation as animation
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

COUNTDOWN_COUNT = 1


class BrownianSimulationForm(QtGui.QMainWindow):

    def __init__(self, main_program, filename):
        super(BrownianSimulationForm, self).__init__()

        # initialise
        self.main_program = main_program
        uic.loadUi('ui/brownian1.ui', self)
        self.button_next.clicked.connect(self.on_button_next_click)
        self.button_play.clicked.connect(self.on_button_play_clicked)

        # initialise graphics
        self.unit_price = 100
        self.period = 60
        self.mu = self.spinbox_mu.value()
        self.sigma = self.spinbox_sigma.value()
        self.interval_time = 0.1
        self.number_of_frames = int(self.period / self.interval_time) + 1

        self.price_x_lower = 0
        self.price_y_lower = 0
        self.price_x_upper = self.period
        self.price_y_upper = self.unit_price * 2

        self.figure_price_id = 99
        self.figure_price = plot.figure(self.figure_price_id)
        self.canvas_price = FigureCanvas(self.figure_price)
        self.layout_graph_simulation.addWidget(self.canvas_price)
        plot.xlim(self.price_x_lower, self.price_x_upper)
        plot.ylim(self.price_y_lower, self.price_y_upper)
        plot.xlabel('Time')
        plot.title('Price per Unit')
        plot.grid()

        f = QFile(filename)
        f.open(QFile.ReadOnly | QFile.Text)
        input_stream = QTextStream(f)
        self.text_edit_instruction.setHtml(input_stream.readAll())
        f.close()

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def on_button_play_clicked(self):
        self.mu = self.spinbox_mu.value()
        self.sigma = self.spinbox_sigma.value()

        self.figure_price.clear()
        max_value = self.plot_price()
        self.price_y_upper = 1.1 * max_value
        plot.xlim(self.price_x_lower, self.price_x_upper)
        plot.ylim(self.price_y_lower, self.price_y_upper)
        plot.xlabel('Time')
        plot.title('Price per Unit')
        plot.grid()
        self.figure_price.canvas.draw()

    def plot_price(self):
        T = self.period
        mu = self.mu
        sigma = self.sigma
        S0 = self.unit_price
        dt = self.interval_time
        N = self.number_of_frames
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        W = np.cumsum(W) * np.sqrt(dt)
        X = (mu - 0.5 * sigma ** 2) * t + sigma * W
        S = S0 * np.exp(X)

        plot.plot(t, S)

        return max(S)

    def on_button_next_click(self):
        self.main_program.show_next_form()

    def countdown(self):
        if self.counter > 0:
            self.button_next.setText("NEXT (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_next.setEnabled(True)
            self.button_next.setText("NEXT")