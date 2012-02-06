import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueCore.CreateUtils as ueCreateUtils

import ueCommon.Open as ueCommonOpen

import ueMaya

class OpenRef(QtGui.QMainWindow):
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

        self.buttonBox.accepted.connect(self.createRef)
        self.buttonBox.rejected.connect(self.close)

    def createRef(self):
        e = ueCommonOpen.getValues()
        maPath = ueCreateUtils.getVersionPath(e[0], e[1], e[2], e[3], e[4], e[5], e[6])
        maFile = ueCreateUtils.getElementName(e[0], e[1], e[2], e[3], e[4], e[5], e[6])
        maya.cmds.file(os.path.join(maPath, maFile+".ma"), r=True)#i=True)#o=True)
        self.close()


class ReferenceEditor(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        self.refList = QtGui.QListWidget()

        toolBar = QtGui.QToolBar()
        createRef = QtGui.QAction("Create reference", self)
        removeRef = QtGui.QAction("Remove reference", self)
        toolBar.addAction(createRef)
        toolBar.addAction(removeRef)

        menuBar = QtGui.QMenuBar()
        menuBar.addMenu("File")

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(toolBar)
        centralWidget.layout().addWidget(self.refList)

        self.setMenuBar(menuBar)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueReference Editor [*]")

        self.connect(createRef, QtCore.SIGNAL("triggered()"), self.refDialog)

    def refDialog(self):
        OpenRef().show()

