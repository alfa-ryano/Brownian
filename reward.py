from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QHeaderView, QTableWidget, QColor, QPalette
from PyQt4.QtCore import QFile, QTextStream, QSize
import os


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

        self.save_results()

        self.table_results.setRowCount(0)
        for result in self.main_program.results:
            if "Practice" in result[0]:
                continue

            row_position = self.table_results.rowCount()
            self.table_results.insertRow(row_position)
            self.table_results.setItem(row_position, 0, QtGui.QTableWidgetItem(str(result[0])))
            self.table_results.setItem(row_position, 1, QtGui.QTableWidgetItem(str(result[1])))
            self.table_results.setItem(row_position, 2, QtGui.QTableWidgetItem(str(result[2])))
            self.table_results.setItem(row_position, 3, QtGui.QTableWidgetItem(str(result[3])))
            self.table_results.setItem(row_position, 4, QtGui.QTableWidgetItem(str(result[4])))
            self.table_results.setItem(row_position, 5, QtGui.QTableWidgetItem(str(result[3])))
            self.table_results.setItem(row_position, 6, QtGui.QTableWidgetItem(str(result[4])))

        self.table_results.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

        self.table_results.horizontalHeaderItem(0).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(1).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(2).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(3).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(4).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(5).setSizeHint(QSize(200, 30))
        self.table_results.horizontalHeaderItem(6).setSizeHint(QSize(200, 30))

    def save_results(self):
        if len(self.main_program.results) > 0:
            data = ["experiment name,fixed compensation,additional compensation,portfolio value,"
                    "benchmark value,gain value,total reward"]

            for result in self.main_program.results:
                row = []
                for item in result:
                    row.append(str(item))

                row = ",".join(row)
                data.append(row)

            folder = "reward"
            filename = "reward_subject " + str(self.main_program.user_id) + "-" + os.environ['COMPUTERNAME'].replace(
                "-", "_") + ".csv"
            filename = filename.replace(" ", "_").lower()
            path = folder + os.sep + filename
            f = open(path, 'w')
            f.write("\n".join(data))
            f.close()

        self.button_close.setEnabled(True)

    def on_button_close(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Warning')
        msg.setText("Are you sure want to exit?\n\nPlease ask the reception desk for further steps.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return_value = msg.exec_()
        if return_value == msg.Yes:
            self.main_program.show_next_form()
