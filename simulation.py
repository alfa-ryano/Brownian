from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import QFile, QTextStream, Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plot
import matplotlib.animation as animation
import numpy as np
import random
import os
import socket
from math import ceil
from customutil import CountDownTimer, format_decimal, COUNTDOWN_COUNT
from brownian2 import BrownianExampleDialog


class ResultDialog(QtGui.QDialog):
    def __init__(self, main_form):
        super(ResultDialog, self).__init__()

        uic.loadUi('ui/result.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.button_next.clicked.connect(self.on_button_next_clicked)

        self.counter = None
        self.countDownTimer = None

    def showEvent(self, show_event):
        super(ResultDialog, self).showEvent(show_event)
        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

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
            super(ResultDialog, self).keyPressEvent(event)

    def on_button_next_clicked(self):
        self.accept()

    def set_result(self, portfolio_value, benchmark_value):
        portfolio_value = round(portfolio_value, 10)
        benchmark_value = round(benchmark_value, 10)
        self.edit_portfolio_value.setText(format_decimal(portfolio_value))
        self.edit_benchmark_value.setText(format_decimal(benchmark_value))
        self.edit_gain_value.setText(format_decimal(portfolio_value - benchmark_value))


class InstructionDialog(QtGui.QDialog):
    def __init__(self, main_form, text, experiment_name):
        super(InstructionDialog, self).__init__()

        uic.loadUi('ui/instruction.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.label_title.setText(experiment_name)
        self.button_ok.clicked.connect(self.on_button_ok_clicked)

        # f = QFile(dialog_file)
        # f.open(QFile.ReadOnly | QFile.Text)
        # input_stream = QTextStream(f)
        # self.text_edit_instruction.setHtml(input_stream.readAll())
        # f.close()
        self.text_edit_instruction.setHtml(text)

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def countdown(self):
        if self.counter > 0:
            self.button_ok.setText("NEXT (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_ok.setEnabled(True)
            self.button_ok.setText("NEXT")

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(InstructionDialog, self).keyPressEvent(event)

    def on_button_ok_clicked(self):
        self.accept()


class InputAssetDialog(QtGui.QDialog):
    def __init__(self, main_form, text, experiment_name):
        super(InputAssetDialog, self).__init__()

        uic.loadUi('ui/dialog.ui', self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.main_form = main_form
        self.label_title.setText(experiment_name)
        self.button_ok.clicked.connect(self.on_button_ok_clicked)

        self.text_edit_instruction.setHtml(text)

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def countdown(self):
        if self.counter > 0:
            self.button_ok.setText("NEXT (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_ok.setEnabled(True)
            self.button_ok.setText("NEXT")

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(InputAssetDialog, self).keyPressEvent(event)

    def on_button_ok_clicked(self):
        self.accept()

    def get_initial_asset_percentage(self):
        value = self.spinbox_asset_value.value()
        return value


class SimulationForm(QtGui.QMainWindow):
    INTERVAL_TIME = 0.1
    X_AXIS_WIDTH = 50

    def __init__(self, main_program, experiment_name, param_simulation_instruction_file, param_dialog_instruction_file,
                 param_portfolio, param_period, param_fix_comp, param_add_comp, param_benchmark_asset, param_interest,
                 param_mu, param_sigma, param_main_instruction_file):
        super(SimulationForm, self).__init__()

        self.experiment_name = experiment_name
        self.mu = param_mu
        self.sigma = param_sigma
        self.current_frame = 0
        self.current_time = 0
        self.fix_compensation = param_fix_comp
        self.add_compensation = param_add_comp
        self.bank_interest = param_interest
        self.period = param_period
        self.number_of_frames = int(self.period / self.INTERVAL_TIME) + 1

        self.W1 = None;
        self.W2 = None;

        # for initialisation the values here are given
        self.initial_portfolio_value = float(param_portfolio)
        self.portfolio_value = self.initial_portfolio_value
        self.portfolio_percentage = self.portfolio_value / self.portfolio_value * 100.0
        self.unit_price = float(random.randint(int(self.initial_portfolio_value * 5.0 / 100.0),
                                               int(self.initial_portfolio_value * 25.0 / 100.0)))

        # main instruction
        text = self.load_instruction(param_main_instruction_file,
                                     param_portfolio, param_interest, self.unit_price, param_benchmark_asset,
                                     param_fix_comp, param_add_comp, param_period, param_mu, param_sigma)
        self.instruction_dialog = InstructionDialog(self, text, self.experiment_name)
        self.instruction_dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.instruction_dialog.setWindowState(QtCore.Qt.WindowMaximized)
        self.instruction_dialog.exec_()
        self.instruction_dialog.close()

        # brownian example dialog
        text = self.load_instruction("instruction/example.html",
                                     param_portfolio, param_interest, self.unit_price, param_benchmark_asset,
                                     param_fix_comp, param_add_comp, param_period, param_mu, param_sigma)
        self.brownian_example_dialog = BrownianExampleDialog(self, text, self.experiment_name, self.mu, self.sigma,
                                                             self.unit_price, self.period,
                                                             self.INTERVAL_TIME, self.X_AXIS_WIDTH)
        self.brownian_example_dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.brownian_example_dialog.setWindowState(QtCore.Qt.WindowMaximized)
        self.brownian_example_dialog.exec_()
        self.brownian_example_dialog.close()

        # set asset dialog
        text = self.load_instruction(param_dialog_instruction_file,
                                     param_portfolio, param_interest, self.unit_price, param_benchmark_asset,
                                     param_fix_comp, param_add_comp, param_period, param_mu, param_sigma)
        self.input_asset_dialog = InputAssetDialog(self, text, self.experiment_name)
        self.input_asset_dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.input_asset_dialog.setWindowState(QtCore.Qt.WindowMaximized)
        self.input_asset_dialog.exec_()
        self.initial_asset_percentage = self.input_asset_dialog.get_initial_asset_percentage()
        self.input_asset_dialog.close()

        # result dialog
        self.result_dialog = ResultDialog(self)
        self.result_dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

        # initialise
        self.main_program = main_program
        self.simulation_started = False
        self.ready_for_next = False
        self.function_animation_price = None
        self.function_animation_delta = None
        self.function_animation_benchmark = None

        self.data_price_equation = np.array([[], []])
        self.data_delta = np.array([[], []])
        self.data_benchmark = np.array([[], []])

        self.data_price = []
        self.data_portfolio = []
        self.data_unit_count = []
        self.data_asset_value = []
        self.data_asset_percentage = []
        self.data_cash_value = []
        self.data_cash_percentage = []

        self.data_benchmark_price = []
        self.data_benchmark_portfolio = []
        self.data_benchmark_unit_count = []
        self.data_benchmark_asset_value = []
        self.data_benchmark_asset_percentage = []
        self.data_benchmark_cash_value = []
        self.data_benchmark_cash_percentage = []

        self.user_data_frame = []
        self.user_data_price = []
        self.user_data_portfolio = []
        self.user_data_benchmark = []
        self.user_data_unit_count = []
        self.user_data_asset_value = []
        self.user_data_asset_percentage = []
        self.user_data_cash_value = []
        self.user_data_cash_percentage = []
        self.user_data_benchmark_unit_count = []
        self.user_data_benchmark_asset_value = []
        self.user_data_benchmark_asset_percentage = []
        self.user_data_benchmark_cash_value = []
        self.user_data_benchmark_cash_percentage = []

        uic.loadUi('ui/simulation.ui', self)
        self.setWindowTitle(experiment_name)
        self.label_title.setText(self.experiment_name)
        self.button_start.clicked.connect(self.on_push_button_start_clicked)
        self.slider_asset.sliderPressed.connect(self.slider_pressed)
        self.slider_asset.mouseReleaseEvent = self.on_mouse_released

        # f = QFile(param_simulation_instruction_file)
        # f.open(QFile.ReadOnly | QFile.Text)
        # input_stream = QTextStream(f)
        # self.text_edit_instruction.setHtml(input_stream.readAll())
        # f.close()
        text = self.load_instruction(param_simulation_instruction_file,
                                     param_portfolio, param_interest, self.unit_price, param_benchmark_asset,
                                     param_fix_comp,
                                     param_add_comp, param_period, param_mu, param_sigma)
        self.text_edit_instruction.setHtml(text)

        # for initialisation the values here are given
        self.asset_percentage = self.initial_asset_percentage
        self.unit_count = self.asset_percentage * self.portfolio_value / (100.0 * self.unit_price)
        self.asset_value = self.unit_price * self.unit_count
        self.cash_value = self.portfolio_value - self.asset_value
        self.cash_percentage = self.portfolio_percentage - self.asset_percentage

        # set benchmark values
        self.benchmark_portfolio_value = self.initial_portfolio_value
        self.benchmark_asset_percentage = param_benchmark_asset
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

        self.record_user_action()

        # initialise graphics
        self.price_x_lower = 0
        self.price_y_lower = 0
        self.price_x_upper = self.X_AXIS_WIDTH
        self.price_y_upper = self.unit_price * 2
        self.price_x_moving_threshold = ceil((self.price_x_lower + self.price_x_upper) * 0.8)

        self.portfolio_x_lower = 0
        self.portfolio_y_lower = 0
        self.portfolio_x_upper = self.X_AXIS_WIDTH
        self.portfolio_y_upper = self.portfolio_value * 2
        self.portfolio_x_moving_threshold = ceil((self.portfolio_x_lower + self.portfolio_x_upper) * 0.8)

        self.figure_price_id = 1
        self.figure_price = plot.figure(self.figure_price_id)
        self.canvas_price = FigureCanvas(self.figure_price)
        self.layoutGraphPrice.addWidget(self.canvas_price)
        self.canvas_price.figure.clear()
        plot.xlim(self.price_x_lower, self.price_x_upper)
        plot.ylim(self.price_y_lower, self.price_y_upper)
        plot.xlabel('Time')
        plot.title('Price per Unit')
        plot.grid()

        self.figure_delta_id = 2
        self.figure_delta = plot.figure(self.figure_delta_id)
        self.canvas_delta = FigureCanvas(self.figure_delta)
        self.layoutGraphDelta.addWidget(self.canvas_delta)
        self.canvas_delta.figure.clear()
        plot.xlim(self.portfolio_x_lower, self.portfolio_x_upper)
        plot.ylim(self.portfolio_y_lower, self.portfolio_y_upper)
        plot.xlabel('Time')
        plot.title('Portfolio Value')
        plot.grid()

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def countdown(self):
        if self.counter > 0:
            self.button_start.setText("START (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_start.setEnabled(True)
            self.button_start.setText("START")

    def on_push_button_start_clicked(self):
        if self.ready_for_next is True:
            self.main_program.show_next_form()
            return

        self.button_start.setEnabled(False)

        if self.function_animation_price is not None:
            self.function_animation_price.event_source.stop()
        self.canvas_price.figure.clear()
        self.figure_price = plot.figure(self.figure_price_id)
        self.data_price_equation = np.array([[], []])
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

        self.record_user_action()

    def slider_pressed(self):
        self.asset_percentage = self.slider_asset.value() / 100.0

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
        self.record_user_action()
        self.update_value_displays()

    def calculate_actual_values(self):
        # self.asset_percentage = self.slider_asset.value() / 100.0
        self.asset_value = self.unit_count * self.unit_price
        self.portfolio_value = self.asset_value + self.cash_value

        to_be_asset_value = self.asset_percentage * self.portfolio_value / 100.0
        to_be_unit_count = to_be_asset_value / self.unit_price

        # record data
        self.data_price.append(self.unit_price)
        self.data_portfolio.append(self.portfolio_value)
        self.data_unit_count.append(self.unit_count)
        self.data_asset_value.append(self.asset_value)
        self.data_asset_percentage.append(self.asset_percentage)
        self.data_cash_value.append(self.cash_value)
        self.data_cash_percentage.append(self.cash_percentage)

        # calculate adjustment of unit count
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

        # record data
        self.data_benchmark_price.append(self.unit_price)
        self.data_benchmark_portfolio.append(self.benchmark_portfolio_value)
        self.data_benchmark_unit_count.append(self.benchmark_unit_count)
        self.data_benchmark_asset_value.append(self.benchmark_asset_value)
        self.data_benchmark_asset_percentage.append(self.benchmark_asset_percentage)
        self.data_benchmark_cash_value.append(self.benchmark_cash_value)
        self.data_benchmark_cash_percentage.append(self.benchmark_cash_percentage)

        # calculate adjustment of unit count
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
        self.edit_price_unit.setText(format_decimal(self.unit_price))
        self.edit_unit_count.setText(format_decimal(self.unit_count))
        self.edit_portfolio_value.setText(format_decimal(self.portfolio_value))
        self.edit_asset_value.setText(format_decimal(self.asset_value))
        self.edit_cash_value.setText(format_decimal(self.cash_value))
        self.edit_asset_percentage.setText(format_decimal(self.asset_percentage))
        self.edit_cash_percentage.setText(format_decimal(self.cash_percentage))

        self.edit_benchmark_value.setText(format_decimal(self.benchmark_portfolio_value))

    def update_line_price(self, num, data, line):
        # create running data for price graphic by filtering the data from index 0 to num.
        # the num is increased by 1 per execution (num is the sequence number of the frame about to be displayed)
        running_data = data[..., :num + 1]
        self.current_frame = num

        # get the last values of x and y of the running data, transform them, and append them to the data for
        # the delta graphic so that delta graphic mirrors price graphic
        if num >= 0:
            last_t = running_data[0][-1]
            last_price = running_data[1][-1]

            self.unit_price = last_price
            self.calculate_values()
            self.update_value_displays()
            self.current_time = int(num * self.INTERVAL_TIME)
            self.edit_time.setText(str(self.current_time))
            self.data_delta = np.insert(self.data_delta,
                                        np.shape(self.data_delta)[1],
                                        [last_t, self.portfolio_value],
                                        axis=1)  # axis: '1' for inserting on matrix column, '0' for row
            self.data_benchmark = np.insert(self.data_benchmark,
                                            np.shape(self.data_benchmark)[1],
                                            [last_t, self.benchmark_portfolio_value],
                                            axis=1)  # axis: '1' for inserting on matrix column, '0' for row

        # print str(self.unit_price) + "\t" + str(self.unit_count) + "\t" + str(self.asset_value)
        # self.data_unit_count.append(self.unit_count)
        # self.data_asset_value.append(self.asset_value)
        # self.data_asset_percentage.append(self.asset_percentage)
        # self.data_cash_value.append(self.cash_value)
        # self.data_cash_percentage.append(self.cash_percentage)
        # self.data_benchmark_unit_count.append(self.benchmark_unit_count)
        # self.data_benchmark_asset_value.append(self.benchmark_asset_value)
        # self.data_benchmark_asset_percentage.append(self.benchmark_asset_percentage)
        # self.data_benchmark_cash_value.append(self.benchmark_cash_value)
        # self.data_benchmark_cash_percentage.append(self.benchmark_cash_percentage)

        # update the price graphic with the running data
        line.set_data(running_data)
        self.update_value_displays()

        # update y-axis
        if self.unit_price > self.price_y_upper * 90.0 / 100.0 or self.unit_price > self.price_y_upper:
            self.price_y_upper += (self.price_y_upper + abs(self.price_y_lower)) * 10 / 100.0
            self.refresh_price_plot()
        if self.unit_price < self.price_y_lower * 10.0 / 100.0 or self.unit_price < self.price_y_lower:
            self.price_y_lower -= (self.price_y_upper + abs(self.price_y_lower)) * 10 / 100.0
            self.refresh_price_plot()

        if self.portfolio_value > self.portfolio_y_upper * 90.0 / 100.0 or self.portfolio_value > self.portfolio_y_upper:
            self.portfolio_y_upper += (self.portfolio_y_upper + abs(self.portfolio_y_lower)) * 10 / 100.0
            self.refresh_delta_plot()
        if self.portfolio_value < self.portfolio_y_lower * 10.0 / 100.0 or self.portfolio_value < self.portfolio_y_lower:
            self.portfolio_y_lower -= (self.portfolio_y_upper + abs(self.portfolio_y_lower)) * 10 / 100.0
            self.refresh_delta_plot()

        if self.benchmark_portfolio_value > self.portfolio_y_upper * 90.0 / 100.0 or \
                self.benchmark_portfolio_value > self.portfolio_y_upper:
            self.portfolio_y_upper += (self.portfolio_y_upper + abs(self.portfolio_y_lower)) * 10 / 100.0
            self.refresh_delta_plot()
        if self.benchmark_portfolio_value < self.portfolio_y_lower * 10.0 / 100.0 or \
                self.benchmark_portfolio_value < self.portfolio_y_lower:
            self.portfolio_y_lower -= (self.portfolio_y_upper + abs(self.portfolio_y_lower)) * 10 / 100.0
            self.refresh_delta_plot()

        # update x-axis
        if self.current_time > self.price_x_moving_threshold and self.price_x_upper < self.period:
            delta = self.current_time - self.price_x_moving_threshold
            self.price_x_lower += delta
            self.price_x_upper += delta
            self.price_x_moving_threshold += delta
            self.refresh_price_plot()

        if self.current_time > self.portfolio_x_moving_threshold and self.portfolio_x_upper < self.period:
            delta = self.current_time - self.portfolio_x_moving_threshold
            self.portfolio_x_lower += delta
            self.portfolio_x_upper += delta
            self.portfolio_x_moving_threshold += delta
            self.refresh_delta_plot()

        if num >= self.number_of_frames - 1:
            # save data
            self.save_data()

            # add result to all results in main_program to be displayed on the last form
            gain_value = self.portfolio_value - self.benchmark_portfolio_value
            reward = 0
            if gain_value < 0:
                reward = self.fix_compensation
            else:
                reward = self.fix_compensation + (self.add_compensation * gain_value)
            result = [self.experiment_name, self.fix_compensation, self.add_compensation,
                      self.portfolio_value, self.benchmark_portfolio_value,
                      gain_value, reward
                      ]
            self.main_program.results.append(result)

            # show end result of current experiment
            self.result_dialog.set_result(self.portfolio_value, self.benchmark_portfolio_value)
            self.result_dialog.exec_()
            self.instruction_dialog.close()

            # enable next button
            self.simulation_started = False
            self.button_start.setEnabled(True)
            self.button_start.setText("NEXT")
            self.ready_for_next = True

    def update_line_delta(self, num, data, line):
        # update the delta graphic with the data_delta calculated in update_line_price function
        line.set_data(self.data_delta)

    def update_line_benchmark(self, num, data, line):
        line.set_data(self.data_benchmark)

    def plot_price(self):
        T = self.period
        mu = self.mu
        sigma = self.sigma
        S0 = self.unit_price  # 20
        dt = self.INTERVAL_TIME
        # dt = 0.1
        # N = round(T / dt) + 1
        N = self.number_of_frames
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size=N)
        self.W1 = W
        W = np.cumsum(W) * np.sqrt(dt)  ### standard brownian motion ###
        self.W2 = W
        X = (mu - 0.5 * sigma ** 2) * t + sigma * W
        S = S0 * np.exp(X)
        x = np.array([t, S])

        self.data_price_equation = x
        l, = plot.plot([], [])
        self.refresh_price_plot()

        self.function_animation_price = animation.FuncAnimation(self.figure_price, self.update_line_price,
                                                                self.number_of_frames,
                                                                fargs=(self.data_price_equation, l),
                                                                interval=self.INTERVAL_TIME * 1000,
                                                                blit=False, repeat=False)
        self.canvas_price.draw()
        self.canvas_price.show()

    def plot_delta(self):

        l, = plot.plot([], [])
        self.refresh_delta_plot()

        self.function_animation_delta = animation.FuncAnimation(self.figure_delta, self.update_line_delta,
                                                                self.number_of_frames,
                                                                fargs=(self.data_delta, l),
                                                                interval=self.INTERVAL_TIME * 1000,
                                                                blit=False, repeat=False)
        self.canvas_delta.draw()
        self.canvas_delta.show()

    def plot_benchmark(self):
        l, = plot.plot([], [])
        self.function_animation_benchmark = animation.FuncAnimation(self.figure_delta, self.update_line_benchmark,
                                                                    self.number_of_frames,
                                                                    fargs=(self.data_benchmark, l),
                                                                    interval=self.INTERVAL_TIME * 1000,
                                                                    blit=False, repeat=False)
        self.canvas_delta.draw()
        self.canvas_delta.show()

    # saving only the actions made
    def save_user_actions(self):
        data = ["second,price,portfolio,unit,asset_v,asset_p,cash_v,cash_p,"
                "b_portfolio,b_unit,b_asset_v,b_asset_p,b_cash_v,b_cash_p,w1,w2"]

        for t in range(0, len(self.user_data_frame)):
            row = [str(self.user_data_frame[t]),
                   str(self.user_data_price[t]),
                   str(self.user_data_portfolio[t]),
                   str(self.user_data_unit_count[t]),
                   str(self.user_data_asset_value[t]),
                   str(self.user_data_asset_percentage[t]),
                   str(self.user_data_cash_value[t]),
                   str(self.user_data_cash_percentage[t]),
                   str(self.user_data_benchmark[t]),
                   str(self.user_data_benchmark_unit_count[t]),
                   str(self.user_data_benchmark_asset_value[t]),
                   str(self.user_data_benchmark_asset_percentage[t]),
                   str(self.user_data_benchmark_cash_value[t]),
                   str(self.user_data_benchmark_cash_percentage[t]),
                   str(self.W1[t]),
                   str(self.W2[t])
                   ]

            row_string = ",".join(row)
            data.append(row_string)

        folder = "decision"
        filename = "decision_subject " + str(self.main_program.user_id) + "-" + str(
            self.windowTitle()) + "-" + socket.gethostname().replace("-", "_") + ".csv"
        filename = filename.replace(" ", "_").lower()
        path = folder + os.sep + filename
        f = open(path, 'w')
        f.write("\n".join(data))
        f.close()

    # saving all data    
    def save_data(self):
        data = ["second,price,portfolio,unit,asset_v,asset_p,cash_v,cash_p,"
                "b_portfolio,b_unit,b_asset_v,b_asset_p,b_cash_v,b_cash_p,w1,w2"]

        prices = self.data_price_equation[1].tolist()
        portfolio_values = self.data_delta[1].tolist()
        benchmark_portfolio_values = self.data_benchmark[1].tolist()

        # append initial configuration
        row = [str(self.user_data_frame[0]),
               str(self.user_data_price[0]),
               str(self.user_data_portfolio[0]),
               str(self.user_data_unit_count[0]),
               str(self.user_data_asset_value[0]),
               str(self.user_data_asset_percentage[0]),
               str(self.user_data_cash_value[0]),
               str(self.user_data_cash_percentage[0]),
               str(self.user_data_benchmark[0]),
               str(self.user_data_benchmark_unit_count[0]),
               str(self.user_data_benchmark_asset_value[0]),
               str(self.user_data_benchmark_asset_percentage[0]),
               str(self.user_data_benchmark_cash_value[0]),
               str(self.user_data_benchmark_cash_percentage[0]),
               str(self.W1[0]),
               str(self.W2[0])
               ]

        row_string = ",".join(row)
        data.append(row_string)

        # append the the rest of the data
        for t in range(0, len(portfolio_values)):
            row = [str(t * self.INTERVAL_TIME),
                   # str(prices[t]),
                   # str(portfolio_values[t]),
                   str(self.data_price[t]),
                   str(self.data_portfolio[t]),
                   str(self.data_unit_count[t]),
                   str(self.data_asset_value[t]),
                   str(self.data_asset_percentage[t]),
                   str(self.data_cash_value[t]),
                   str(self.data_cash_percentage[t]),
                   str(self.data_benchmark_portfolio[t]),
                   str(self.data_benchmark_unit_count[t]),
                   str(self.data_benchmark_asset_value[t]),
                   str(self.data_benchmark_asset_percentage[t]),
                   str(self.data_benchmark_cash_value[t]),
                   str(self.data_benchmark_cash_percentage[t]),
                   str(self.W1[t]),
                   str(self.W2[t]),
                   ]

            row_string = ",".join(row)
            data.append(row_string)

        folder = "result"
        filename = "result_subject-" + str(self.main_program.user_id) + "-" + str(
            self.windowTitle()) + "-" + socket.gethostname().replace("-", "_") + ".csv"
        filename = filename.replace(" ", "_").lower()
        path = folder + os.sep + filename
        f = open(path, 'w')
        f.write("\n".join(data))
        f.close()

    def refresh_price_plot(self):
        self.figure_price = plot.figure(self.figure_price_id)
        plot.xlim(self.price_x_lower, self.price_x_upper)
        plot.ylim(self.price_y_lower, self.price_y_upper)
        plot.xlabel('Time')
        plot.title('Price per Unit')
        plot.grid()

    def refresh_delta_plot(self):
        self.figure_delta = plot.figure(self.figure_delta_id)
        plot.xlim(self.portfolio_x_lower, self.portfolio_x_upper)
        plot.ylim(self.portfolio_y_lower, self.portfolio_y_upper)
        plot.xlabel('Time')
        plot.title('Portfolio Value')
        plot.grid()

    def record_user_action(self):
        self.user_data_frame.append(self.current_frame * self.INTERVAL_TIME)
        self.user_data_price.append(self.unit_price)
        self.user_data_portfolio.append(self.portfolio_value)
        self.user_data_unit_count.append(self.unit_count)
        self.user_data_asset_value.append(self.asset_value)
        self.user_data_asset_percentage.append(self.asset_percentage)
        self.user_data_cash_value.append(self.cash_value)
        self.user_data_cash_percentage.append(self.cash_percentage)
        self.user_data_benchmark.append(self.benchmark_portfolio_value)
        self.user_data_benchmark_unit_count.append(self.benchmark_unit_count)
        self.user_data_benchmark_asset_value.append(self.benchmark_asset_value)
        self.user_data_benchmark_asset_percentage.append(self.benchmark_asset_value)
        self.user_data_benchmark_cash_value.append(self.benchmark_cash_value)
        self.user_data_benchmark_cash_percentage.append(self.benchmark_cash_percentage)

    def load_instruction(self, filename,
                         param_portfolio, param_interest, unit_price, param_benchmark_asset, param_fix_comp,
                         param_add_comp, param_period, param_mean, param_sigma):
        file = open(filename, 'r')
        text = file.read()
        text = text.replace("[portfolio]", format_decimal(param_portfolio))
        text = text.replace("[interest]", format_decimal(param_interest))
        text = text.replace("[price]", format_decimal(unit_price))
        text = text.replace("[b_asset]", format_decimal(param_benchmark_asset))
        text = text.replace("[1 - b_asset]", format_decimal(100 - param_benchmark_asset))
        text = text.replace("[fixed_comp]", format_decimal(param_fix_comp))
        text = text.replace("[add_comp]", format_decimal(param_add_comp))
        text = text.replace("[period/60]", format_decimal(param_period / 60))
        text = text.replace("[mean]", format_decimal(param_mean))
        text = text.replace("[sigma]", format_decimal(param_sigma))

        return text
