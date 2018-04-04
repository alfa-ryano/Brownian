import sys
from PyQt4 import QtGui, QtCore
from register import RegisterForm
from simulation import SimulationForm
# import ConfigParser

class MainProgram:
    INDEX_FORM_TYPE = 0
    INDEX_FORM_TITLE = 1
    INDEX_FORM_INSTRUCTION = 2
    INDEX_FORM_DIALOG = 3
    INDEX_CONF_FILE = 4

    def __init__(self):
        self.app = None
        self.user_id = None

        self.form_confs = []
        # self.form_confs.append([RegisterForm.__name__, "", "", ""])
        self.form_confs.append(
            [SimulationForm.__name__, "Simulation 01", "instruction/simulation_01.html", "instruction/dialog_01.html",
             "configuration/simulation_01.ini"])
        self.form_confs.append(
            [SimulationForm.__name__, "Simulation 02", "instruction/simulation_02.html", "instruction/dialog_02.html",
             "configuration/simulation_02.ini"])
        self.form_confs.append(
            [SimulationForm.__name__, "Simulation 03", "instruction/simulation_03.html", "instruction/dialog_03.html",
             "configuration/simulation_03.ini"])
        self.current_form_index = 0
        self.current_form = None

    def start(self):
        form_conf = self.form_confs[self.current_form_index]
        if form_conf[self.INDEX_FORM_TYPE] == RegisterForm.__name__:
            self.current_form = RegisterForm(self)
        elif form_conf[self.INDEX_FORM_TYPE] == SimulationForm.__name__:
            self.current_form = SimulationForm(self, form_conf[self.INDEX_FORM_TITLE],
                                               form_conf[self.INDEX_FORM_INSTRUCTION],
                                               form_conf[self.INDEX_FORM_DIALOG], form_conf[self.INDEX_CONF_FILE])

        self.current_form.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.current_form.showMaximized()

    def show_next_form(self):
        self.current_form.close()
        self.current_form_index += 1

        if self.current_form_index >= len(self.form_confs):
            self.terminate()
            return

        form_conf = self.form_confs[self.current_form_index]
        if form_conf[self.INDEX_FORM_TYPE] == RegisterForm.__name__:
            self.current_form = RegisterForm(self)
        elif form_conf[self.INDEX_FORM_TYPE] == SimulationForm.__name__:
            self.current_form = SimulationForm(self, form_conf[self.INDEX_FORM_TITLE],
                                               form_conf[self.INDEX_FORM_INSTRUCTION],
                                               form_conf[self.INDEX_FORM_DIALOG], form_conf[self.INDEX_CONF_FILE])

        self.current_form.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.current_form.showMaximized()

    def terminate(self):
        self.app.quit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_program = MainProgram()
    main_program.app = app
    main_program.start()
    sys.exit(app.exec_())
