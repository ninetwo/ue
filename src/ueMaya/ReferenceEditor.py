import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCommon.Open as ueCommonOpen
import ueMaya

__ueclasses__ = ["ms", "geo", "cam"]

global refEditor

class OpenRef(QtGui.QMainWindow):
    def __init__(self, redrawRefList=False, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        self.redrawRefList = redrawRefList

        ueCommonOpen.setClasses(__ueclasses__)

        self.openWidget = ueCommonOpen.Open()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.openWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueOpenReference [*]")

        self.buttonBox.accepted.connect(self.createRef)
        self.buttonBox.rejected.connect(self.close)

    def createRef(self):
        spec = ueCommonOpen.getValues()
        version = ueAssetUtils.getVersions(spec)[int(spec.vers)-1]
        if spec.elclass == "geo":
            ext = "obj"
        elif spec.elclass == "cam":
            ext = "fbx"
        else:
            ext = "ma"
        maya.cmds.file(os.path.join(version["path"], version["file_name"]+"."+ext),
                       namespace=version["file_name"], r=True)
        if self.redrawRefList:
            refEditor.drawRefList()
        self.close()


class ReferenceEditor(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        global refEditor
        refEditor = self

        self.refList = QtGui.QListWidget()

        self.drawRefList()

        createRef = QtGui.QAction("Create reference", self)
        removeRef = QtGui.QAction("Remove reference", self)

        # Menubar
        menuBar = QtGui.QMenuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(createRef)
        fileMenu.addAction(removeRef)

        # Toolbar
        toolBar = QtGui.QToolBar()
        toolBar.addAction(createRef)
        toolBar.addAction(removeRef)

        # Reference list
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(toolBar)
        centralWidget.layout().addWidget(self.refList)

        self.setMenuBar(menuBar)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueReferenceEditor [*]")

        self.connect(createRef, QtCore.SIGNAL("triggered()"), self.createRef)
        self.connect(removeRef, QtCore.SIGNAL("triggered()"), self.removeRef)

    def drawRefList(self):
        refs = maya.cmds.ls(references=True)
        self.refList.clear()
        for ref in refs:
            self.refList.addItem(QtGui.QListWidgetItem(ref))

    def createRef(self):
        OpenRef(redrawRefList=True).show()

    def removeRef(self):
        ref = str(self.refList.currentItem().text())
        maya.cmds.file(removeReference=True, referenceNode=ref)
        self.drawRefList()

