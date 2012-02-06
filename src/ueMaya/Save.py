import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueMaya
import ueMaya.Utilities as ueMayaUtils

import ueCommon.Save as ueCommonSave

def ueSave():
    if maya.cmds.file(q=True, sn=True) == "":
        ueSaveAs()
        return

    maya.cmds.file(save=True, type="mayaAscii")

def ueSaveVers():
    if maya.cmds.file(q=True, sn=True) == "":
        ueSaveAs()
        return

    fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

    spec = ueSpec.Spec(fi["ueproj"], fi["uegrp"], fi["ueasst"],
                       fi["ueclass"], fi["uetype"], fi["uename"])

    ueMayaUtils.saveUtility(spec)

def ueSaveAs():
    Save().show()


class Save(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonSave.setClasses(["s"])

        self.saveWidget = ueCommonSave.Save()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.saveWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueSave [*]")

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        spec = ueCommonSave.getValues()
        ueMayaUtils.saveUtility(spec)
        self.close()

