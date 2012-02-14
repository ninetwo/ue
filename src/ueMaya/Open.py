import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueMaya
import ueCommon.Open as ueCommonOpen
import ueCore.AssetUtils as ueAssetUtils

__ueclasses__ = ["ms"]

class Open(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonOpen.setClasses(__ueclasses__)

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
        spec = ueCommonOpen.getValues()
        maPath = ueAssetUtils.getVersionPath(spec)
        maFile = ueAssetUtils.getElementName(spec)
        maya.cmds.file(os.path.join(maPath, maFile+".ma"), o=True, f=True)
        print "Opened %s" % spec
        self.close()

