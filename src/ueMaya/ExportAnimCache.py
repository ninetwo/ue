import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueMaya
import ueMaya.Utilities as ueMayaUtils
import ueCommon.Save as ueCommonSave

__exportTypes__ = {
                   "Selected":            ("selected", ["cam", "lgt", "geo", "mrs", "ms"]),
                   "Camera":              ("cameras",  ["cam"]),
                   "Light":               ("lights",   ["lgt"]),
                   "Geometry":            ("geometry", ["geo"]),
                   "Shading Group (mr)":  ("mrShader", ["mrs"])
                  }

def ueExportAnimCache():
    ExportAnimCache().show()


class ExportAnimCache(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonSave.setClasses([])

        self.itemMenu = QtGui.QListWidget()
        self.itemMenu.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        exportWidget = QtGui.QGroupBox("Export")
        exportWidget.setLayout(QtGui.QHBoxLayout())

        exportWidget.layout().addWidget(QtGui.QLabel("Item"))
        exportWidget.layout().addWidget(self.itemMenu)
        
        self.saveWidget = ueCommonSave.Save()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(exportWidget)
        centralWidget.layout().addWidget(self.saveWidget)
        centralWidget.layout().addWidget(buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueExportAnimCache [*]")

        self.setExport()

        buttonBox.accepted.connect(self.export)
        buttonBox.rejected.connect(self.close)

    def setExport(self):
        self.saveWidget.elclasses = ["geo"]
        self.saveWidget.loadClasses()
        items = maya.cmds.ls(geometry=True)
        self.itemMenu.clear()
        for i in items:
            self.itemMenu.addItem(QtGui.QListWidgetItem(i))

    def export(self):
        spec, dbMeta = ueCommonSave.getValues()
        selection = []
        for i in self.itemMenu.selectedItems():
            selection.append(i.text())
        maya.cmds.select(selection, ne=True, r=True)
        ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="obj", export=True, animated=True)
        spec.elclass = "ms"
        ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
#        ueFileUtils.deleteFiles(os.path.join(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")))
        self.close()

