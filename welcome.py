from PyQt4 import QtGui, uic
from customutil import CountDownTimer

COUNTDOWN_COUNT = 1


class WelcomeForm(QtGui.QMainWindow):

    def __init__(self, main_program):
        super(WelcomeForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/welcome.ui', self)
        self.button_next.clicked.connect(self.on_button_next_click)

        self.counter = COUNTDOWN_COUNT
        self.countDownTimer = CountDownTimer(10, 0, 1, self.countdown)
        self.countDownTimer.start()

    def countdown(self):
        if self.counter > 0:
            self.button_next.setText("Next (" + str(self.counter) + ")")
            self.counter -= 1
        else:
            self.countDownTimer.stop()
            self.button_next.setEnabled(True)
            self.button_next.setText("Next")

    def on_button_next_click(self):
        self.main_program.show_next_form()
