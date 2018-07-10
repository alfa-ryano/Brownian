from PyQt4 import QtGui, uic
from PyQt4.QtCore import QFile, QTextStream
from customutil import CountDownTimer

COUNTDOWN_COUNT = 1


class IntermediaryForm(QtGui.QMainWindow):

    def __init__(self, main_program, message, filename):
        super(IntermediaryForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/intermediary.ui', self)
        self.button_next.clicked.connect(self.on_button_next_click)

        self.message = message
        self.button_next.setText(self.message)

        f = QFile(filename)
        f.open(QFile.ReadOnly | QFile.Text)
        input_stream = QTextStream(f)
        self.text_edit_instruction.setHtml(input_stream.readAll())
        f.close()

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def on_button_next_click(self):
        self.main_program.show_next_form()

    def countdown(self):
        if self.counter > 0:
            self.button_next.setText(self.message + " (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_next.setEnabled(True)
            self.button_next.setText(self.message)