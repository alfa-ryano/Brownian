from PyQt4 import QtGui, uic


class RegisterForm(QtGui.QMainWindow):

    def __init__(self, main_program):
        super(RegisterForm, self).__init__()
        self.main_program = main_program
        uic.loadUi('register.ui', self)
        self.main_program.user_id = self.edit_id.text()
        self.button_next.clicked.connect(self.on_button_next_click)

    def on_button_next_click(self):
            self.main_program.show_next_form()
