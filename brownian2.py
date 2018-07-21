from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import Qt
from customutil import CountDownTimer, format_decimal
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plot


COUNTDOWN_COUNT = 1


class BrownianExampleDialog(QtGui.QDialog):

    def __init__(self, main_form, text, experiment_name, param_mu, param_sigma, param_unit_price, param_period,
                 param_interval_time, x_axis_width):
        super(BrownianExampleDialog, self).__init__()

        uic.loadUi('ui/brownian2.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.label_title.setText(experiment_name)
        self.button_next.clicked.connect(self.on_button_next_clicked)

        self.text_edit_instruction.setHtml(text)

        # initialise graphics
        self.unit_price = param_unit_price
        self.period = param_period
        self.mu = param_mu
        self.sigma = param_sigma
        self.interval_time = param_interval_time
        self.number_of_frames = int(self.period / self.interval_time) + 1
        
        self.price_x_lower = 0
        self.price_y_lower = 0
        self.price_x_upper = x_axis_width
        # self.price_y_upper = self.unit_price * 2

        layouts = [self.layout_graph_1, self.layout_graph_2, self.layout_graph_3, 
                   self.layout_graph_4, self.layout_graph_5, self.layout_graph_6]

        for index in range(0,6):
            self.figure_price_id = "a" + str(index)
            self.figure_price = plot.figure(self.figure_price_id)
            self.canvas = FigureCanvas(self.figure_price)
            layouts[index].addWidget(self.canvas)
            self.canvas.figure.clear()

            max_value = self.plot_price()

            plot.xlim(self.price_x_lower, self.price_x_upper)
            self.price_y_upper = 1.1 * max_value
            plot.ylim(self.price_y_lower, self.price_y_upper)
            plot.xlabel('Time (seconds)')
            plot.title('Price per Unit')
            plot.grid()

            self.canvas.draw()
            self.canvas.show()

        # start timer
        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

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

    def countdown(self):
        if self.counter > 0:
            self.button_next.setText("NEXT (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_next.setEnabled(True)
            self.button_next.setText("NEXT")

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(BrownianExampleDialog, self).keyPressEvent(event)

    def on_button_next_clicked(self):
        self.accept()

