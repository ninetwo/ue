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

global selected

def ueExport(export="Selected"):
    global selected
    selected = export
    Export().show()


class Export(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonSave.setClasses([])

        self.exportMenu = QtGui.QListWidget()
        self.itemMenu = QtGui.QListWidget()
        self.itemMenu.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        for et in __exportTypes__:
            self.exportMenu.addItem(QtGui.QListWidgetItem(et))

        exportWidget = QtGui.QGroupBox("Export")
        exportWidget.setLayout(QtGui.QGridLayout())

        exportWidget.layout().addWidget(QtGui.QLabel("Export"), 0, 0)
        exportWidget.layout().addWidget(self.exportMenu, 1, 0)
        exportWidget.layout().addWidget(QtGui.QLabel("Item"), 0, 1)
        exportWidget.layout().addWidget(self.itemMenu, 1, 1)
        
        self.saveWidget = ueCommonSave.Save()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(exportWidget)
        centralWidget.layout().addWidget(self.saveWidget)
        centralWidget.layout().addWidget(buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueExport [*]")

        self.exportMenu.setCurrentItem(self.exportMenu.findItems(selected,
                                       QtCore.Qt.MatchExactly)[0])
        self.setExport()

        buttonBox.accepted.connect(self.export)
        buttonBox.rejected.connect(self.close)
        self.exportMenu.itemSelectionChanged.connect(self.setExport)

    def setExport(self):
        t = __exportTypes__[str(self.exportMenu.currentItem().text())]
        self.saveWidget.elclasses = t[1]
        self.saveWidget.loadClasses()
        if t[0] == "selected":
            items = maya.cmds.ls(selection=True)
        elif t[0] == "cameras":
            items = maya.cmds.ls(cameras=True)
        elif t[0] == "lights":
            items = maya.cmds.ls(lights=True)
        elif t[0] == "geometry":
            items = maya.cmds.ls(geometry=True)
        elif t[0] == "mrShader":
            items = maya.cmds.ls(type="shadingEngine")
        self.itemMenu.clear()
        for i in items:
            self.itemMenu.addItem(QtGui.QListWidgetItem(i))

    def export(self):
        spec, dbMeta = ueCommonSave.getValues()
        selection = []
        for i in self.itemMenu.selectedItems():
            selection.append(i.text())
        maya.cmds.select(selection)
        if spec.elclass == "ms":
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
        elif spec.elclass == "cam":
            spec.elclass = "ms"
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
            spec.elclass = "cam"
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="fbx", export=True)
        elif spec.elclass == "lgt":
            spec.elclass = "ms"
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
            spec.elclass = "lgt"
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="fbx", export=True)
        elif spec.elclass == "geo":
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="obj", export=True)
            spec.elclass = "ms"
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
        elif spec.elclass == "mrs":
            ueMayaUtils.saveUtility(spec, dbMeta=dbMeta, fileType="ma", export=True)
#        ueFileUtils.deleteFiles(os.path.join(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")))
        self.close()

