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

        self.checkArea = QtGui.QWidget()
        self.checkArea.setLayout(QtGui.QGridLayout())

        self.layout().addWidget(self.checkArea)
        self.runChecks()
        self.layout().addStretch(0)

    def runChecks(self):
        # Clear out the checkArea layout before repopulating it
        for i in range(self.checkArea.layout().count()):
            self.checkArea.layout().itemAt(i).widget().close()

        self.toUpdate = {}

        n = 0

        self.checkArea.layout().addWidget(QtGui.QLabel("Current\nvalue"), n, 1)
        self.checkArea.layout().addWidget(QtGui.QLabel("Project\nvalue"), n, 2)

        n += 1
        for check in self.checks:
            c = self.checks[check]

            updateqt = []
            updateqt.append(QtGui.QLabel(c["desc"]))
            updateqt.append(QtGui.QLabel(str(eval(c["curval"]))))
            updateqt.append(QtGui.QLabel(str(eval(c["newval"]))))
            updateqt.append(QtGui.QPushButton(""))

            for i, item in enumerate(updateqt):
                self.checkArea.layout().addWidget(item, n, i)

            if (lambda: eval(c["eval"]))():
                updateqt[3].setText("Update")
                self.connect(updateqt[3], QtCore.SIGNAL("clicked()"),
                             lambda x=c, y=updateqt, z=check: self.update(x, y, z))
                self.toUpdate[check] = {"cmd": c, "qt": updateqt}
            else:
                updateqt[3].setText("Up to date")
                updateqt[3].setEnabled(False)

            n += 1

        checkButton = QtGui.QPushButton("Check")
        self.updateButton = QtGui.QPushButton("Update All")

        if len(self.toUpdate) == 0:
            self.updateButton.setEnabled(False)

        self.checkArea.layout().addWidget(checkButton, n, 0, 1, 3)
        self.checkArea.layout().addWidget(self.updateButton, n, 3)

        self.connect(checkButton,
                     QtCore.SIGNAL("clicked()"),
                     self.runChecks)

        self.connect(self.updateButton,
                     QtCore.SIGNAL("clicked()"),
                     self.updateAll)

    def update(self, c, q, i):
        eval(c["update"])
        q[1].setText(str(eval(c["curval"])))
        q[3].setEnabled(False)
        q[3].setText("Up to date")
        del self.toUpdate[i]
        if len(self.toUpdate) == 0:
            self.updateButton.setEnabled(False)

    def updateAll(self):
        n = []
        for update in self.toUpdate:
            n.append(update)
        for i in n:
            self.update(self.toUpdate[i]["cmd"], self.toUpdate[i]["qt"], i)

