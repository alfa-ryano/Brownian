from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox


class WelcomeForm(QtGui.QMainWindow):

    def __init__(self, main_program):
        super(WelcomeForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/welcome.ui', self)
        self.button_next.clicked.connect(self.on_button_next_click)

    def on_button_next_click(self):
        self.main_program.show_next_form()