from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QHeaderView, QTableWidget, QColor, QPalette
from PyQt4.QtCore import QFile, QTextStream, QSize
import os
import random
from customutil import EventTimer


class RewardForm(QtGui.QMainWindow):
    def __init__(self, main_program):
        super(RewardForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/reward.ui', self)

        self.random_selected_case = 0
        self.label_id.setText(self.main_program.user_id)
        self.label_computer_name.setText(os.environ['COMPUTERNAME'])

        f = QFile("instruction/reward.html")
        f.open(QFile.ReadOnly | QFile.Text)
        input_stream = QTextStream(f)
        self.text_edit_instruction.setHtml(input_stream.readAll())
        f.close()

        self.button_close.clicked.connect(self.on_button_close)
        self.button_start_shuffling.clicked.connect(self.on_button_start_shuffling_clicked)
        self.button_stop_shuffling.clicked.connect(self.on_button_stop_shuffling_clicked)

        self.table_results.setRowCount(0)
        for result in self.main_program.results:
            row_position = self.table_results.rowCount()
            self.table_results.insertRow(row_position)
            self.table_results.setItem(row_position, 0, QtGui.QTableWidgetItem(str(result[0])))
            self.table_results.setItem(row_position, 1, QtGui.QTableWidgetItem(str(result[1])))
            self.table_results.setItem(row_position, 2, QtGui.QTableWidgetItem(str(result[2])))
            self.table_results.setItem(row_position, 3, QtGui.QTableWidgetItem(str(result[3])))
            self.table_results.setItem(row_position, 4, QtGui.QTableWidgetItem(str(result[4])))

        self.table_results.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

        self.table_results.horizontalHeaderItem(0).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(1).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(2).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(3).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(4).setSizeHint(QSize(200, 30))

        if self.table_results.rowCount() > 0:
            self.timer = EventTimer(0.05, self.update_random_number)

    def on_button_start_shuffling_clicked(self):
        self.button_start_shuffling.setEnabled(False)
        self.button_stop_shuffling.setEnabled(True)
        if self.table_results.rowCount() > 0:
            self.timer.start()

    def on_button_stop_shuffling_clicked(self):
        if self.table_results.rowCount() > 0:
            self.timer.stop()
            row_index = self.random_selected_case - 1
            self.table_results.selectRow(row_index)
            for column_index in range(self.table_results.columnCount()):
                cell = self.table_results.item(row_index, column_index)
                if cell is None:
                    cell = QtGui.QTableWidgetItem()
                    self.table_results.setItem(row_index, column_index, cell)
                cell.setBackground(QColor(200, 200, 200))

            data = []
            for item in self.main_program.results[row_index]:
                data.append(str(item))
            data = [",".join(data)]

            folder = "result"
            filename = str(self.main_program.user_id) + "-" + str(
                self.windowTitle()) + "-user-" + os.environ['COMPUTERNAME'].replace("-", "_") + "_reward.csv"
            filename = filename.replace(" ", "_").lower()
            path = folder + os.sep + filename
            f = open(path, 'w')
            f.write("\n".join(data))
            f.close()

        self.button_stop_shuffling.setEnabled(False)
        self.button_close.setEnabled(True)


    def on_button_close(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Warning')
        msg.setText("Are you sure want to exit?\n\nPlease print the screen or take a picture of the result "
                    "as a proof for your reward.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return_value = msg.exec_()
        if return_value == msg.Yes:
            self.main_program.show_next_form()

    def update_random_number(self):
        # random_selected_case = random.randint(1,5)
        self.random_selected_case = random.randint(1, self.table_results.rowCount())
        self.label_random_number.setText(str(self.random_selected_case))



