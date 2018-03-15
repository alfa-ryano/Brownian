# -*- coding: utf-8 -*-
"""
Project: Framework for a Dynamic Brownian Motion
September 2014
@author: georgalosk
contact: k.georgalos@lancaster.ac.uk
"""
from __future__ import division
from __future__ import unicode_literals
from PyQt4 import QtGui, QtCore
import numpy as np
from math import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import csv
import random
from time import *
import threading
import time
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Window(QtGui.QMainWindow):


    def __init__(self):        
        QtGui.QMainWindow.__init__(self)
        super(Window,self).__init__()

        self.line_ani = None
        
        #dimension of exec screens
        self.setGeometry(10,10,1020,748)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)  #close buttons
        self.button = QtGui.QPushButton('Plot',self)
        self.button.setGeometry(10,670,150,50)
        
        #this creates the frame where the plot appears        
        self.frame_graph = QtGui.QFrame(self)
        self.frame_graph.setGeometry(QtCore.QRect(400,230, 520,450))
       # self.frame_graph.setFrameShape(QtGui.QFrame.NoFrame)
        self.graph_layout = QtGui.QVBoxLayout(self.frame_graph)
        #this creates the canvas where the plot appears
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graph_layout.addWidget(self.canvas)
        self.button.clicked.connect(self.plotb)
     #   self.button.clicked.connect(self.button.hide)
        
    def plotb(self):
        def update_line(num, data, line):
            line.set_data(data[...,:num])
            return line,
    
        if self.line_ani != None:
            self.line_ani.event_source.stop()
            self.graph_layout.removeWidget(self.canvas)            
            self.figure = plt.figure()
            self.canvas = FigureCanvas(self.figure)
            self.graph_layout.addWidget(self.canvas)
            
     #   self.figure = plt.figure()
        T = 100
        mu = 0.0
        sigma = 0.1
        S0 = 20
        dt = 0.1
        N = round(T/dt)
        t = np.linspace(0, T, N)
        W = np.random.standard_normal(size = N)
        W = np.cumsum(W)*np.sqrt(dt) ### standard brownian motion ###
        X = (mu-0.5*sigma**2)*t + sigma*W
        S = S0*np.exp(X)
        x = np.array([t, S])

        data = x
        l, = plt.plot([], [])
        plt.xlim(0, 100)
        plt.ylim(0, 45)
        plt.xlabel('time')
        plt.title('price')
       #plot the exercise price
        ep=[0]*1000
        plt.plot(t,ep,"r",linewidth=3.0)

        plt.grid()

        self.line_ani = animation.FuncAnimation(self.figure, update_line, 1000, fargs=(data, l),
            interval=20, blit=False,repeat=False)
        self.canvas.draw()
        self.canvas.show()  
      
       # plt.show()     
#EXECUTION:        
###############################################################################
###############################################################################
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)

    win = Window()
    win.show()
    #win.showMaximized()
    app.installEventFilter(win)   
    sys.exit(app.exec_())# -*- coding: utf-8 -*-

