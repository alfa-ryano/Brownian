from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
import ConfigParser

COUNTDOWN_COUNT = 1


class WelcomeForm(QtGui.QMainWindow):

    def __init__(self, main_program):
        super(WelcomeForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/welcome.ui', self)
        self.button_next.clicked.connect(self.on_button_next_click)

    def on_button_next_click(self):
        config = ConfigParser.RawConfigParser()
        config.read('configuration/application.conf')
        locked = int(config.getfloat('CONFIG', 'locked'))
        if locked == 0:
            self.main_program.show_next_form()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Information')
            msg.setText("The application is still locked. You will be informed when the application is already opened "
                        "by the administrator.")
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.exec_()
