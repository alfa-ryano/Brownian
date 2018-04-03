from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QFile, QTextStream
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import numpy as np


class InputAssetDialog(QtGui.QDialog):
    def __init__(self, main_form, dialog_file):
        super(InputAssetDialog, self).__init__()
        uic.loadUi('ui/dialog.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.button_ok.clicked.connect(self.on_button_ok_clicked)

        f = QFile(dialog_file)
        f.open(QFile.ReadOnly | QFile.Text)
        input_stream = QTextStream(f)
        self.text_edit_instruction.setHtml(input_stream.readAll())
        f.close()

    def on_button_ok_clicked(self):
        self.accept()

    def get_initial_asset_percentage(self):
        value = self.spinbox_asset_value.value()
        return value

class SimulationForm(QtGui.QMainWindow):
    TIME_INTERVAL = 1  # in milliseconds
    NUMBER_OF_FRAMES = 1000

    def __init__(self, main_program, title, instruction_file, dialog_file):
        super(SimulationForm, self).__init__()

        # dialog
        self.input_asset_dialog = InputAssetDialog(self, dialog_file)
        self.input_asset_dialog.exec_()
        self.initial_asset_percentage = self.input_asset_dialog.get_initial_asset_percentage()
        self.input_asset_dialog.close()

        # initialise
        self.main_program = main_program
        self.simulation_started = False
        self.ready_for_next = False
        self.function_animation_price = None
        self.function_animation_delta = None
        self.function_animation_benchmark = None
        self.data_price = np.array([[], []])
        self.data_delta = np.array([[], []])
        self.data_benchmark = np.array([[], []])

        uic.loadUi('ui/simulation.ui', self)
        self.setWindowTitle(title)
        self.button_start.clicked.connect(self.on_push_button_start_clicked)
        self.slider_asset.sliderPressed.connect(self.slider_pressed)
        self.slider_asset.mouseReleaseEvent = self.on_mouse_released

        file = QFile(instruction_file)
        file.open(QFile.ReadOnly | QFile.Text)
        input_stream = QTextStream(file)
        self.text_edit_instruction.setHtml(input_stream.readAll())
        file.close()

        # for initialisation the values here are given
        self.initial_portfolio_value = 100.0
        self.portfolio_value = self.initial_portfolio_value
        self.portfolio_percentage = self.portfolio_value / self.portfolio_value * 100.0
        self.unit_price = 25.0
        self.asset_percentage = self.initial_asset_percentage
        self.unit_count = self.asset_percentage * self.portfolio_value / (100.0 * self.unit_price)
        self.asset_value = self.unit_price * self.unit_count
        self.cash_value = self.portfolio_value - self.asset_value
        self.cash_percentage = self.portfolio_percentage - self.asset_percentage

        # set benchmark values
        self.benchmark_portfolio_value = self.initial_portfolio_value
        self.benchmark_asset_percentage = 20.0
        self.benchmark_unit_count = self.benchmark_asset_percentage * self.benchmark_portfolio_value / (
            100.0 * self.unit_price)
        self.benchmark_asset_value = self.unit_price * self.benchmark_unit_count
        self.benchmark_cash_value = self.benchmark_portfolio_value - self.benchmark_asset_value
        self.benchmark_portfolio_percentage = self.benchmark_portfolio_value / self.benchmark_portfolio_value * 100.0
        self.benchmark_cash_percentage = self.benchmark_portfolio_percentage - self.benchmark_asset_percentage

        # init values displayed
        self.slider_asset.setSliderPosition(self.asset_percentage * 100.0)
        self.update_value_displays()
        self.edit_time.setText(str(0))

        # initialise graphics
        self.figure_price_id = 1
        self.figure_price = plot.figure(self.figure_price_id)
        self.canvas_price = FigureCanvas(self.figure_price)
        self.layoutGraphPrice.addWidget(self.canvas_price)
        self.canvas_price.figure.clear()
        plot.xlim(0, 100)
        plot.ylim(0, 50)
        plot.xlabel('period')
        plot.title('price per unit')
        plot.grid()

        self.figure_delta_id = 2
        self.figure_delta = plot.figure(self.figure_delta_id)
        self.canvas_delta = FigureCanvas(self.figure_delta)
        self.layoutGraphDelta.addWidget(self.canvas_delta)
        self.canvas_delta.figure.clear()
        plot.xlim(0, 100)
        plot.ylim(0, 200)
        plot.xlabel('period')
        plot.title('portfolio value')
        plot.grid()

    def on_push_button_start_clicked(self):
        if self.ready_for_next is True:
            self.main_program.show_next_form()
            return

        self.button_start.setEnabled(False)
        if self.function_animation_price is not None:
            self.function_animation_price.event_source.stop()
        self.canvas_price.figure.clear()
        self.figure_price = plot.figure(self.figure_price_id)
        self.data_price = np.array([[], []])
        self.plot_price()

        if self.function_animation_delta is not None:
            self.function_animation_delta.event_source.stop()

        if self.function_animation_benchmark is not None:
            self.function_animation_benchmark.event_source.stop()

        self.canvas_delta.figure.clear()
        self.figure_delta = plot.figure(self.figure_delta_id)
        self.data_delta = np.array([[], []])
        self.plot_delta()

        self.figure_delta = plot.figure(self.figure_delta_id)
        self.data_benchmark = np.array([[], []])
        self.plot_benchmark()

        self.simulation_started = True

    def slider_pressed(self):
        self.asset_percentage = self.slider_asset.value() / 100.0
        print "slider pressed"

    def on_mouse_released(self, mouse_event):
        left_margin = 6
        right_margin = 6
        total_margin = left_margin + right_margin
        x = mouse_event.x()
        width = self.slider_asset.width() - total_margin
        unit = width / 10000.0
        pos = round((x - left_margin) / unit)
        self.slider_asset.setValue(pos)

        self.asset_percentage = self.slider_asset.value() / 100.0
        self.calculate_values()
        self.update_value_displays()
        print "mouse released"

    def calculate_actual_values(self):
        # self.asset_percentage = self.slider_asset.value() / 100.0
        self.asset_value = self.unit_count * self.unit_price
        self.portfolio_value = self.asset_value + self.cash_value

        to_be_asset_value = self.asset_percentage * self.portfolio_value / 100.0
        to_be_unit_count = to_be_asset_value / self.unit_price

        if to_be_unit_count < self.unit_count:
            delta_unit_count = self.unit_count - to_be_unit_count
            if delta_unit_count > self.unit_count:
                delta_unit_count = self.unit_count
            self.unit_count -= delta_unit_count
            delta_cash_value = delta_unit_count * self.unit_price
            self.cash_value += delta_cash_value
        elif to_be_unit_count > self.unit_count:
            delta_unit_count = to_be_unit_count - self.unit_count
            max_affordable_unit_to_buy = self.cash_value / self.unit_price
            if delta_unit_count > max_affordable_unit_to_buy:
                delta_unit_count = max_affordable_unit_to_buy
            self.unit_count += delta_unit_count
            delta_cash_value = delta_unit_count * self.unit_price
            self.cash_value -= delta_cash_value
            if self.cash_value < 0.000000000001:
                self.cash_value = 0

        self.asset_value = to_be_asset_value
        self.cash_percentage = self.cash_value / self.portfolio_value * 100.0

    def calculate_benchmark_values(self):
        self.benchmark_asset_value = self.benchmark_unit_count * self.unit_price
        self.benchmark_portfolio_value = self.benchmark_asset_value + self.benchmark_cash_value

        to_be_benchmark_asset_value = self.benchmark_asset_percentage * self.benchmark_portfolio_value / 100.0
        to_be_benchmark_unit_count = to_be_benchmark_asset_value / self.unit_price

        if to_be_benchmark_unit_count < self.benchmark_unit_count:
            delta_benchmark_unit_count = self.benchmark_unit_count - to_be_benchmark_unit_count
            if delta_benchmark_unit_count > self.benchmark_unit_count:
                delta_benchmark_unit_count = self.benchmark_unit_count
            self.benchmark_unit_count -= delta_benchmark_unit_count
            delta_benchmark_cash_value = delta_benchmark_unit_count * self.unit_price
            self.benchmark_cash_value += delta_benchmark_cash_value
        elif to_be_benchmark_unit_count > self.benchmark_unit_count:
            delta_benchmark_unit_count = to_be_benchmark_unit_count - self.benchmark_unit_count
            max_affordable_benchmark_unit_to_buy = self.benchmark_cash_value / self.unit_price
            if delta_benchmark_unit_count > max_affordable_benchmark_unit_to_buy:
                delta_benchmark_unit_count = max_affordable_benchmark_unit_to_buy
            self.benchmark_unit_count += delta_benchmark_unit_count
            delta_benchmark_cash_value = delta_benchmark_unit_count * self.unit_price
            self.benchmark_cash_value -= delta_benchmark_cash_value
            if self.benchmark_cash_value < 0.000000000001:
                self.benchmark_cash_value = 0

        self.benchmark_asset_value = to_be_benchmark_asset_value
        self.benchmark_cash_percentage = self.benchmark_cash_value / self.benchmark_portfolio_value * 100.0

    def calculate_values(self):
        self.calculate_benchmark_values()
        self.calculate_actual_values()

    def update_value_displays(self):
        self.edit_price_unit.setText(str(self.unit_price))
        self.edit_unit_count.setText(str(self.unit_count))
        self.edit_portfolio_value.setText(str(self.portfolio_value))
        self.edit_asset_value.setText(str(self.asset_value))
        self.edit_cash_value.setText(str(self.cash_value))
        self.edit_asset_percentage.setText(str(self.asset_percentage))
        self.edit_cash_percentage.setText(str(self.cash_percentage))

        self.edit_benchmark_value.setText(str(self.benchmark_portfolio_value))

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
                                        axis=1)  # axis: '1' for inserting on matrix column, '0' for row
            self.data_benchmark = np.insert(self.data_benchmark,
                                            np.shape(self.data_benchmark)[1],
                                            [last_t, self.benchmark_portfolio_value],
                                            axis=1)  # axis: '1' for inserting on matrix column, '0' for row

        # update the price graphic with the running data
        line.set_data(running_data)
        self.update_value_displays()

        print num
        if num >= self.NUMBER_OF_FRAMES - 1:
            self.simulation_started = False
            self.button_start.setEnabled(True)
            self.button_start.setText("Next")
            self.ready_for_next = True

    def update_line_delta(self, num, data, line):
        # update the delta graphic with the data_delta calculated in update_line_price function
        line.set_data(self.data_delta)

    def update_line_benchmark(self, num, data, line):
        line.set_data(self.data_benchmark)

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
        plot.xlabel('period')
        plot.title('price per unit')
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
        plot.xlabel('period')
        plot.title('portfolio value')
        plot.grid()

        self.function_animation_delta = animation.FuncAnimation(self.figure_delta, self.update_line_delta,
                                                                self.NUMBER_OF_FRAMES,
                                                                fargs=(self.data_delta, l),
                                                                interval=self.TIME_INTERVAL,
                                                                blit=False, repeat=False)
        self.canvas_delta.draw()
        self.canvas_delta.show()

    def plot_benchmark(self):
        l, = plot.plot([], [])
        self.function_animation_benchmark = animation.FuncAnimation(self.figure_delta, self.update_line_benchmark,
                                                                    self.NUMBER_OF_FRAMES,
                                                                    fargs=(self.data_benchmark, l),
                                                                    interval=self.TIME_INTERVAL,
                                                                    blit=False, repeat=False)
        self.canvas_delta.draw()
        self.canvas_delta.show()
