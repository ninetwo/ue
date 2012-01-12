from PyQt4 import QtCore, QtGui

import ueMaya
import ueMaya.Utilities as ueMayaUtils

import ueCommon.Save as ueCommonSave

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
        ueMayaUtils.saveUtility(e[0], e[1], e[2], e[3], e[4], e[5])
        self.close()

