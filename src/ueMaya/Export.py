import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueMaya
import ueMaya.Utilities as ueMayaUtils
import ueMaya.Save as ueMayaSave
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
        self.exportAsSeparateElements = QtGui.QCheckBox("Export selection as seperate elements?")
        self.exportAsSeparateElements.setChecked(False)
        self.exportCache = QtGui.QCheckBox("Export cache?")
        self.exportCache.setChecked(True)

        for et in __exportTypes__:
            self.exportMenu.addItem(QtGui.QListWidgetItem(et))

        exportWidget = QtGui.QGroupBox("Export")
        exportWidget.setLayout(QtGui.QGridLayout())

        exportOptionsWidget = QtGui.QGroupBox("Export Options")
        exportOptionsWidget.setLayout(QtGui.QVBoxLayout())

        exportWidget.layout().addWidget(QtGui.QLabel("Export"), 0, 0)
        exportWidget.layout().addWidget(self.exportMenu, 1, 0)
        exportWidget.layout().addWidget(QtGui.QLabel("Item"), 0, 1)
        exportWidget.layout().addWidget(self.itemMenu, 1, 1)

        exportOptionsWidget.layout().addWidget(self.exportAsSeparateElements)
        exportOptionsWidget.layout().addWidget(self.exportCache)

        self.saveWidget = ueCommonSave.Save()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(exportWidget)
        centralWidget.layout().addWidget(exportOptionsWidget)
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
        destSpec, dbMeta = ueCommonSave.getValues()

        fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

        sourceSpec = ueSpec.Spec(fi["ueproj"], fi["uegrp"], fi["ueasst"],
                                 fi["ueclass"], fi["uetype"], fi["uename"],
                                 fi["uevers"])

        dbMeta["comment"] = "Exported from %s" % str(sourceSpec)

        # Get the selected nodes from the dialog list
        selection = []
        for i in self.itemMenu.selectedItems():
            selection.append(str(i.text()))

        # If we're exporting all our seleted items into one element,
        # add the entire list into another list so when we iterate over
        # it, we return the list once and export everything
        if not self.exportAsSeparateElements.isChecked():
            newSelection = []
            newSelection.append(selection)
            selection = newSelection

        # Iterate over our selection and export
        if destSpec.elclass == "ms":
            for item in selection:
                if self.exportAsSeparateElements.isChecked():
                    destSpec.elname = item.replace(":", "")
                maya.cmds.select(item, r=True)
                ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="ma", export=True)
        elif destSpec.elclass == "cam":
            for item in selection:
                if self.exportAsSeparateElements.isChecked():
                    destSpec.elname = item.replace(":", "")
                maya.cmds.select(item, r=True)
                destSpec.elclass = "ms"
                ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="ma", export=True)
                if self.exportCache.isChecked():
                    destSpec.elclass = "cam"
                    ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="fbx", export=True)
        elif destSpec.elclass == "lgt":
            for item in selection:
                if self.exportAsSeparateElements.isChecked():
                    destSpec.elname = item.replace(":", "")
                maya.cmds.select(item, r=True)
                destSpec.elclass = "ms"
                ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="ma", export=True)
                if self.exportCache.isChecked():
                    destSpec.elclass = "lgt"
                    ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="fbx", export=True)
        elif destSpec.elclass == "geo":
            for item in selection:
                if self.exportAsSeparateElements.isChecked():
                    destSpec.elname = item.replace(":", "")
                maya.cmds.select(item, r=True)
                destSpec.elclass = "ms"
                ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="ma", export=True)
                if self.exportCache.isChecked():
                    destSpec.elclass = "geo"
                    ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="obj", export=True)
        elif destSpec.elclass == "mrs":
            for item in selection:
                if self.exportAsSeparateElements.isChecked():
                    destSpec.elname = item.replace(":", "")
                maya.cmds.select(item, r=True)
                ueMayaUtils.saveUtility(destSpec, dbMeta=dbMeta, fileType="ma", export=True)

#        ueFileUtils.deleteFiles(os.path.join(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")))

        self.close()

