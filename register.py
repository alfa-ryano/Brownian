from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox


class RegisterForm(QtGui.QMainWindow):

    def __init__(self, main_program):
        super(RegisterForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('ui/register.ui', self)
        self.main_program.user_id = None
        self.button_next.clicked.connect(self.on_button_next_click)

    def on_button_next_click(self):
        self.main_program.user_id = str(self.edit_id.text()).strip()
        if len(self.main_program.user_id) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("ID cannot be empty!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        if not self.main_program.user_id.isdigit():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("ID can only contain numeric characters!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        self.main_program.show_next_form()