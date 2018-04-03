import wx
import sys
from PyQt4 import QtGui, uic
from register import RegisterForm
from simulation import SimulationForm


class MainProgram:
    def __init__(self):
        self.app = None
        self.user_id = None

        self.forms = []
        # self.forms.append(RegisterForm(self))
        self.forms.append(SimulationForm(self))
        self.current_form_index = 0
        self.current_form = self.forms[self.current_form_index]

    def start(self):
        self.current_form.showMaximized()

    def show_next_form(self):
        self.current_form.close()
        self.current_form_index += 1
        self.current_form = self.forms[self.current_form_index]
        self.current_form.showMaximized()

    def exit(self):
        for form in self.forms:
            if form is not None:
                form.close()
        application = QtGui.QApplication(sys.argv)
        sys.exit(application.exec_())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_program = MainProgram()
    main_program.start()
    sys.exit(app.exec_())
