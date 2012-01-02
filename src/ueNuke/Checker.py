import sys, os

from PyQt4 import QtCore, QtGui

import nuke, nukescripts

import ueNuke

checker = ueNuke.checker

class CheckerPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())

        self.checks = checker["nuke"]

        self.checkButton = QtGui.QPushButton("Check")

        head = QtGui.QWidget()
        head.setLayout(QtGui.QHBoxLayout())
        head.layout().addWidget(QtGui.QLabel("Item"))
        head.layout().addWidget(QtGui.QLabel("Current value"))
        head.layout().addWidget(QtGui.QLabel("New value"))
        head.layout().addWidget(QtGui.QLabel("Update"))

        foot = QtGui.QWidget()
        foot.setLayout(QtGui.QHBoxLayout())
        foot.layout().addWidget(self.checkButton)

        self.layout().addWidget(head)
        self.load()
        self.layout().addWidget(foot)

#        self.connect(self.checkButton,
#                     QtCore.SIGNAL("clicked()"),
#                     self.load)

    def load(self):
        for check in self.checks:
            c = self.checks[check]
            if (lambda: eval(c["eval"]))():
                this = QtGui.QWidget()

                this.setLayout(QtGui.QHBoxLayout())
                this.layout().addWidget(QtGui.QLabel(c["desc"]))
                this.layout().addWidget(QtGui.QLabel(str((lambda: eval(c["curval"]))())))
                this.layout().addWidget(QtGui.QLabel(str((lambda: eval(c["newval"]))())))
                this.layout().addWidget(QtGui.QPushButton("Update"))

                self.layout().addWidget(this)

