import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCommon.Open as ueCommonOpen
import ueMaya

__ueclasses__ = ["ms", "geo", "cam", "lgt", "mrs"]

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
        elif spec.elclass == "lgt":
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

        self.classList = QtGui.QListWidget()
        self.typeList = QtGui.QListWidget()
        self.refList = QtGui.QListWidget()

        self.buildRefDict()

        self.drawClassList()
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

        # Main area
        mainWidget = QtGui.QWidget()
        mainWidget.setLayout(QtGui.QGridLayout())
        mainWidget.layout().addWidget(QtGui.QLabel("class"), 0, 0)
        mainWidget.layout().addWidget(QtGui.QLabel("type"), 0, 1)
        mainWidget.layout().addWidget(self.classList, 1, 0)
        mainWidget.layout().addWidget(self.typeList, 1, 1)
        mainWidget.layout().addWidget(self.refList, 2, 0, 1, 2)

        # Reference list
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(toolBar)
        centralWidget.layout().addWidget(mainWidget)

        self.setMenuBar(menuBar)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueReferenceEditor [*]")

        self.connect(createRef, QtCore.SIGNAL("triggered()"), self.createRef)
        self.connect(removeRef, QtCore.SIGNAL("triggered()"), self.removeRef)

    def buildRefDict(self):
        refs = maya.cmds.ls(references=True)
        self.refDict = {}
        for ref in refs:
            refName = maya.cmds.referenceQuery(ref, filename=True, shortName=True)
            refElement = refName.split("_")
            if not refElement[5] in self.refDict:
                self.refDict[refElement[5]] = {}
            if not refElement[4] in self.refDict[refElement[5]]:
                self.refDict[refElement[5]][refElement[4]] = {}
            if not refElement[3] in self.refDict[refElement[5]][refElement[4]]:
                self.refDict[refElement[5]][refElement[4]][refElement[3]] = []
            vers = int(refElement[6].split(".")[0])
            spec = ueSpec.Spec(proj=refElement[0], grp=refElement[1], asst=refElement[2],
                               elclass=refElement[5], eltype=refElement[4], elname=refElement[3],
                               vers=vers)
            self.refDict[refElement[5]][refElement[4]][refElement[3]].append(spec)

    def drawClassList(self):
        self.classList.clear()
        if len(self.refDict) > 0:
            for elclass in self.refDict:
                self.classList.addItem(QtGui.QListWidgetItem(elclass))
            self.classList.setCurrentItem(self.classList.item(0))
            self.drawTypeList()

    def drawTypeList(self):
        self.typeList.clear()
        if len(self.refDict[str(self.classList.currentItem().text())]) > 0:
            for eltype in self.refDict[str(self.classList.currentItem().text())]:
                self.typeList.addItem(QtGui.QListWidgetItem(eltype))
            self.typeList.setCurrentItem(self.typeList.item(0))

    def drawRefList(self):
        self.refList.clear()
        for elclass in self.refDict:
            for eltype in self.refDict[elclass]:
                for elname in self.refDict[elclass][eltype]:
                    for vers in self.refDict[elclass][eltype][elname]:
                        self.refList.addItem(QtGui.QListWidgetItem(str(vers)))

    def createRef(self):
        OpenRef(redrawRefList=True).show()

    def removeRef(self):
        ref = str(self.refList.currentItem().text())
        maya.cmds.file(removeReference=True, referenceNode=ref)
        self.drawRefList()

