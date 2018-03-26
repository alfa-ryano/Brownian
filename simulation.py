from PyQt4 import QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import numpy as np


class SimulationForm(QtGui.QMainWindow):
    TIME_INTERVAL = 1000  # in milliseconds
    NUMBER_OF_FRAMES = 1000

    def __init__(self, main_program):
        super(SimulationForm, self).__init__()
        self.main_program = main_program

        self.timer = None
        self.function_animation_price = None
        self.function_animation_delta = None
        self.data_price = np.array([[], []])
        self.data_delta = np.array([[], []])
        self.adjustmentValue = 0

        uic.loadUi('simulation.ui', self)
        self.buttonStart.clicked.connect(self.on_push_button_start_clicked)
        self.slider_asset.valueChanged.connect(self.on_slider_asset_value_changed)

        # for initialisation the values here are given
        self.portfolio_value = 100.0
        self.portfolio_percentage = self.portfolio_value / self.portfolio_value * 100.0
        self.unit_price = 25.0
        self.asset_percentage = 50
        self.unit_count = self.asset_percentage * self.portfolio_value / (100.0 * self.unit_price)
        self.asset_value = self.unit_price * self.unit_count
        self.cash_value = self.portfolio_value - self.asset_value
        self.cash_percentage = self.portfolio_percentage - self.asset_percentage

        self.slider_asset.setSliderPosition(self.asset_percentage)
        self.update_value_displays()
        self.edit_time.setText(str(0))

        self.figure_price_id = 1
        self.figure_price = plot.figure(self.figure_price_id)
        self.canvas_price = FigureCanvas(self.figure_price)
        self.layoutGraphPrice.addWidget(self.canvas_price)
        plot.xlim(0, 100)
        plot.ylim(0, 50)
        plot.xlabel('time')
        plot.title('price')
        plot.grid()

        self.figure_delta_id = 2
        self.figure_delta = plot.figure(self.figure_delta_id)
        self.canvas_delta = FigureCanvas(self.figure_delta)
        self.layoutGraphDelta.addWidget(self.canvas_delta)
        plot.xlim(0, 100)
        plot.ylim(0, 200)
        plot.xlabel('time')
        plot.title('total assets')
        plot.grid()

        print "constructor executed"

    def on_push_button_start_clicked(self):
        if self.function_animation_price is not None:
            self.function_animation_price.event_source.stop()
        self.canvas_price.figure.clear()
        self.figure_price = plot.figure(self.figure_price_id)
        self.data_price = np.array([[], []])
        self.plot_price()

        if self.function_animation_delta is not None:
            self.function_animation_delta.event_source.stop()
        self.canvas_delta.figure.clear()
        self.figure_delta = plot.figure(self.figure_delta_id)
        self.data_delta = np.array([[], []])
        self.plot_delta()

        print "Button Start clicked"

    def on_slider_asset_value_changed(self):
        self.calculate_values()
        self.update_value_displays()
        print "Slider Asset value changed"

    def calculate_values(self):
        self.asset_percentage = self.slider_asset.value()
        self.asset_value = self.unit_count * self.unit_price
        self.portfolio_value = self.asset_value + self.cash_value

        to_be_asset_value = self.asset_percentage * self.portfolio_value / 100.0
        to_be_unit_count = to_be_asset_value / self.unit_price

        if to_be_unit_count < self.unit_count:
            delta_unit_count = self.unit_count - to_be_unit_count
            self.unit_count -= delta_unit_count
            total_new_cash = delta_unit_count * self.unit_price
            self.cash_value += total_new_cash
        elif to_be_unit_count > self.unit_count:
            delta_unit_count = to_be_unit_count - self.unit_count
            self.unit_count +=delta_unit_count
            total_new_cash = delta_unit_count * self.unit_price
            self.cash_value -= total_new_cash

        self.cash_percentage = self.cash_value / self.portfolio_value * 100

    def update_value_displays(self):
        self.edit_price_unit.setText(str(self.unit_price))
        self.edit_portfolio_value.setText(str(self.portfolio_value))
        self.edit_asset_value.setText(str(self.asset_value))
        self.edit_cash_value.setText(str(self.cash_value))
        self.edit_asset_percentage.setText(str(self.asset_percentage))
        self.edit_cash_percentage.setText(str(self.cash_percentage))

    def update_line_price(self, num, data, line):
        # create running data for price graphic by filtering the data from index 0 to num.
        # the num is increased by 1 per execution (num is the sequence number of the frame about to be displayed)
        running_data = data[..., :num]

        # get the last values of x and y of the running data, transform them, and append them to the data for
        # the delta graphic so that delta graphic mirrors price graphic
        if num > 0:
            last_t = running_data[0][-1]
            last_price = running_data[1][-1]

            self.unit_price = last_price
            self.calculate_values()
            self.update_value_displays()
            self.edit_time.setText(str(num))
            self.data_delta = np.insert(self.data_delta,
                                        np.shape(self.data_delta)[1],
                                        [last_t, self.portfolio_value],
                                        axis=1)  # axis: '1' for inserting on column, '0' for row

        # update the price graphic with the running data
        line.set_data(running_data)
        self.update_value_displays()

    def update_line_delta(self, num, data, line):
        # update the delta graphic with the data_delta calculated in update_line_price function
        line.set_data(self.data_delta)

    def plot_price(self):
        T = 100
        mu = 0.0
        sigma = 0.1
        S0 = self.unit_price  # 20
        dt = 0.1
        N = round(T / dt)
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
        X = (mu - 0.5 * sigma ** 2) * t + sigma * W
        S = S0 * np.exp(X)
        x = np.array([t, S])

        self.data_price = x
        l, = plot.plot([], [])
        plot.xlim(0, 100)
        plot.ylim(0, 50)
        plot.xlabel('time')
        plot.title('price')
        plot.grid()

        self.function_animation_price = animation.FuncAnimation(self.figure_price, self.update_line_price,
                                                                self.NUMBER_OF_FRAMES,
                                                                fargs=(self.data_price, l),
                                                                interval=self.TIME_INTERVAL,
                                                                blit=False, repeat=False)
        self.canvas_price.draw()
        self.canvas_price.show()

    def plot_delta(self):
        l, = plot.plot([], [])
        plot.xlim(0, 100)
        plot.ylim(0, 200)
        plot.xlabel('time')
        plot.title('total assets')
        plot.grid()

        self.function_animation_delta = animation.FuncAnimation(self.figure_delta, self.update_line_delta,
                                                                self.NUMBER_OF_FRAMES,
                                                                fargs=(self.data_delta, l),
                                                                interval=self.TIME_INTERVAL,
                                                                blit=False, repeat=False)
        self.canvas_delta.draw()
        self.canvas_delta.show()

# if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     window = Main()
#     # window.show()
#     window.showMaximized()
#     sys.exit(app.exec_())
