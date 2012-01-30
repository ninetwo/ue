import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueMaya
import ueMaya.Utilities as ueMayaUtils

import ueCommon.Save as ueCommonSave

def ueSave():
    maya.cmds.file(save=True, type="mayaAscii")

def ueSaveVers():
    fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

    proj = fi["proj"]
    grp = fi["grp"]
    asst = fi["asst"]
    elclass = fi["elclass"]
    eltype = fi["eltype"]
    name = fi["elname"]

    ueMayaUtils.saveUtility(proj, grp, asst, elclass, eltype, name)

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
        e = ueCommonSave.getValues()

        maya.cmds.fileInfo("proj", e[0])
        maya.cmds.fileInfo("grp", e[1])
        maya.cmds.fileInfo("asst", e[2])
        maya.cmds.fileInfo("elclass", e[3])
        maya.cmds.fileInfo("eltype", e[4])
        maya.cmds.fileInfo("elname", e[5])
        maya.cmds.fileInfo("asst_root", os.getenv("ASST_ROOT"))

        ueMayaUtils.saveUtility(e[0], e[1], e[2], e[3], e[4], e[5])
        self.close()

