import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueMaya

import ueCommon.Open as ueCommonOpen

import ueCore.CreateUtils as ueCreateUtils

class Open(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonOpen.setClasses(["s"])

        self.openWidget = ueCommonOpen.Open()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.openWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueOpen [*]")

        self.buttonBox.accepted.connect(self.open)
        self.buttonBox.rejected.connect(self.close)

    def open(self):
        e = ueCommonOpen.getValues()
        maPath = ueCreateUtils.getVersionPath(e[0], e[1], e[2], e[3], e[4], e[5], e[6])
        maFile = ueCreateUtils.getElementName(e[0], e[1], e[2], e[3], e[4], e[5], e[6])
        maya.cmds.file(os.path.join(maPath, maFile+".ma"), i=True)#o=True)
        self.close()

