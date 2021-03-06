import sys
from PyQt4 import QtGui, QtCore

from intermediary import IntermediaryForm
from register import RegisterForm
from simulation import SimulationForm
from reward import RewardForm
from welcome import WelcomeForm
from general import GeneralInstructionForm
import csv
from brownian1 import BrownianSimulationForm


# import ConfigParser

class MainProgram:
    INDEX_FORM_TYPE = 0
    INDEX_FORM_TITLE = 1
    INDEX_DIALOG_INSTRUCTION = 2
    INDEX_SIMULATION_INSTRUCTION = 3
    INDEX_PORTFOLIO = 4
    INDEX_PERIOD = 5
    INDEX_FIX_COMPENSATION = 6
    INDEX_ADD_COMPENSATION = 7
    INDEX_BENCHMARK_ASSET = 8
    INDEX_BANK_INTEREST = 9
    INDEX_MU = 10
    INDEX_SIGMA = 11
    INDEX_MAIN_INSTRUCTION = 12

    WAIT_TIME = 10

    INDEX_GENERAL_INSTRUCTION_FILENAME = 1;
    INDEX_INTERMEDIARY_FORM_MESSAGE = 1;
    INDEX_INTERMEDIARY_FORM_FILENAME = 2;

    NUMBER_OF_PRACTICES = 2

    results = []

    def __init__(self):
        self.app = None
        self.user_id = None

        self.form_confs = []
        self.form_confs.append([RegisterForm.__name__, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
        self.form_confs.append([WelcomeForm.__name__, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
        self.form_confs.append(
            [GeneralInstructionForm.__name__, "instruction/general_01.html", "2", "3", "4", "5", "6", "7", "8", "9",
             "10", "11"])
        self.form_confs.append(
            [GeneralInstructionForm.__name__, "instruction/general_02.html", "2", "3", "4", "5", "6", "7", "8", "9",
             "10", "11"])
        self.form_confs.append(
            [GeneralInstructionForm.__name__, "instruction/general_03.html", "2", "3", "4", "5", "6", "7", "8", "9",
             "10", "11"])
        self.form_confs.append(
            [BrownianSimulationForm.__name__, "instruction/simulation.html", "2", "3", "4", "5", "6", "7", "8", "9",
             "10", "11"])
        self.form_confs.append(
            [IntermediaryForm.__name__, "Start Practice!", "instruction/start_practice.html", "3", "4", "5", "6", "7",
             "8", "9", "10", "11"])

        with open("configuration/simulation_configuration.csv", "r") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader, None)  # skip header
            for i, line in enumerate(reader):

                configuration = [None] * 13
                configuration[self.INDEX_FORM_TYPE] = SimulationForm.__name__
                configuration[self.INDEX_FORM_TITLE] = str(line[0]).strip()
                configuration[self.INDEX_PORTFOLIO] = float(line[1])
                configuration[self.INDEX_PERIOD] = float(line[2])
                configuration[self.INDEX_FIX_COMPENSATION] = float(line[3])
                configuration[self.INDEX_ADD_COMPENSATION] = float(line[4])
                configuration[self.INDEX_BENCHMARK_ASSET] = float(line[5])
                configuration[self.INDEX_BANK_INTEREST] = float(line[6])
                configuration[self.INDEX_DIALOG_INSTRUCTION] = "instruction/" + str(line[7]).strip()
                configuration[self.INDEX_SIMULATION_INSTRUCTION] = "instruction/" + str(line[8]).strip()
                configuration[self.INDEX_MU] = float(line[9])
                configuration[self.INDEX_SIGMA] = float(line[10])
                configuration[self.INDEX_MAIN_INSTRUCTION] = "instruction/" + str(line[11]).strip()
                self.form_confs.append(configuration)

                if (i + 1) == self.NUMBER_OF_PRACTICES:
                    self.form_confs.append(
                        [IntermediaryForm.__name__, "Start Simulation!", "instruction/start_simulation.html", "3", "4",
                         "5", "6", "7", "8", "9", "10",
                         "11"])

        self.form_confs.append([RewardForm.__name__, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])

        self.current_form_index = 0
        self.current_form = None

    def start(self):
        form_conf = self.form_confs[self.current_form_index]
        if form_conf[self.INDEX_FORM_TYPE] == RegisterForm.__name__:
            self.current_form = RegisterForm(self)
        elif form_conf[self.INDEX_FORM_TYPE] == WelcomeForm.__name__:
            self.current_form = WelcomeForm(self)
        elif form_conf[self.INDEX_FORM_TYPE] == BrownianSimulationForm.__name__:
            filename = form_conf[self.INDEX_GENERAL_INSTRUCTION_FILENAME]
            self.current_form = BrownianSimulationForm(self, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == GeneralInstructionForm.__name__:
            filename = form_conf[self.INDEX_GENERAL_INSTRUCTION_FILENAME]
            self.current_form = GeneralInstructionForm(self, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == IntermediaryForm.__name__:
            message = form_conf[self.INDEX_INTERMEDIARY_FORM_MESSAGE]
            filename = form_conf[self.INDEX_INTERMEDIARY_FORM_FILENAME]
            self.current_form = IntermediaryForm(self, message, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == SimulationForm.__name__:
            self.current_form = SimulationForm(self, form_conf[self.INDEX_FORM_TITLE],
                                               form_conf[self.INDEX_SIMULATION_INSTRUCTION],
                                               form_conf[self.INDEX_DIALOG_INSTRUCTION],
                                               form_conf[self.INDEX_PORTFOLIO],
                                               form_conf[self.INDEX_PERIOD],
                                               form_conf[self.INDEX_FIX_COMPENSATION],
                                               form_conf[self.INDEX_ADD_COMPENSATION],
                                               form_conf[self.INDEX_BENCHMARK_ASSET],
                                               form_conf[self.INDEX_BANK_INTEREST],
                                               form_conf[self.INDEX_MU],
                                               form_conf[self.INDEX_SIGMA],
                                               form_conf[self.INDEX_MAIN_INSTRUCTION]
                                               )

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
        elif form_conf[self.INDEX_FORM_TYPE] == WelcomeForm.__name__:
            self.current_form = WelcomeForm(self)
        elif form_conf[self.INDEX_FORM_TYPE] == BrownianSimulationForm.__name__:
            filename = form_conf[self.INDEX_GENERAL_INSTRUCTION_FILENAME]
            self.current_form = BrownianSimulationForm(self, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == GeneralInstructionForm.__name__:
            filename = form_conf[self.INDEX_GENERAL_INSTRUCTION_FILENAME]
            self.current_form = GeneralInstructionForm(self, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == IntermediaryForm.__name__:
            message = form_conf[self.INDEX_INTERMEDIARY_FORM_MESSAGE]
            filename = form_conf[self.INDEX_INTERMEDIARY_FORM_FILENAME]
            self.current_form = IntermediaryForm(self, message, filename)
        elif form_conf[self.INDEX_FORM_TYPE] == SimulationForm.__name__:
            self.current_form = SimulationForm(self, form_conf[self.INDEX_FORM_TITLE],
                                               form_conf[self.INDEX_SIMULATION_INSTRUCTION],
                                               form_conf[self.INDEX_DIALOG_INSTRUCTION],
                                               form_conf[self.INDEX_PORTFOLIO],
                                               form_conf[self.INDEX_PERIOD],
                                               form_conf[self.INDEX_FIX_COMPENSATION],
                                               form_conf[self.INDEX_ADD_COMPENSATION],
                                               form_conf[self.INDEX_BENCHMARK_ASSET],
                                               form_conf[self.INDEX_BANK_INTEREST],
                                               form_conf[self.INDEX_MU],
                                               form_conf[self.INDEX_SIGMA],
                                               form_conf[self.INDEX_MAIN_INSTRUCTION]
                                               )
        elif form_conf[self.INDEX_FORM_TYPE] == RewardForm.__name__:
            self.current_form = RewardForm(self)

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
