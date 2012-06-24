from PyQt4 import QtGui, QtCore

from rv import rvtypes, commands

import ueSpec

import ueEdit

from ueCore import AssetUtils as ueAssetUtils
from ueQt import AssetWidgets as ueAssetWidgets

class ToolBox(QtGui.QToolBar):
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)

        self.parent = parent

        self.setWindowTitle("Tool Box")

        button = QtGui.QToolButton()
        self.addWidget(button)

        a = QtGui.QAction("test", self)
        button.addAction(a)
        button.connect(a, QtCore.SIGNAL("triggered()"), self.load)

    def load(self):
        retimeNodes = []
	for source in commands.nodesOfType("RVSourceGroup"):
		node = commands.newNode("RVRetimeGroup", "%sRetime" % source)
		commands.setNodeInputs(node, [source])
                retimeNodes.append(node)
                commands.setViewNode(node)
                nodes = commands.nodesInGroup(node)
                if "%s_retime" % node in nodes:
                    properties =  commands.properties("%s_retime" % node)
                    if "%s_retime.visual.scale" % node in properties:
                        commands.setFloatProperty("%s_retime.visual.scale" % node, [4.0], False)
        commands.setNodeInputs("defaultSequence", retimeNodes)
        commands.setViewNode("defaultSequence")


class AbstractEdit(QtGui.QDockWidget):
    def __init__(self, editType, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec
        self.spec.elclass = "edt"
        self.spec.eltype = editType

        self.shotWidget = ueAssetWidgets.QUeShotMenuWidget(spec)
        self.editMenu = QtGui.QComboBox()
        self.editVersionsMenu = QtGui.QComboBox()
        self.newEdit = QtGui.QLineEdit()
        self.addNewEdit = QtGui.QPushButton("Add")
        self.editTree = QtGui.QTreeWidget()
        self.addGroup = QtGui.QPushButton("Add Group")
        self.addAsset = QtGui.QPushButton("Add Asset")
        self.update = QtGui.QPushButton("Edit")
        self.importEdit = QtGui.QPushButton("Import Edit")
        self.createAllButton = QtGui.QPushButton("Create/Update All")
        self.createSelectedButton = QtGui.QPushButton("Create/Update Selected")
        self.saveEditButton = QtGui.QPushButton("Save Edit")

        editWidget = QtGui.QWidget()
        editWidget.setLayout(QtGui.QHBoxLayout())
        editWidget.layout().addWidget(self.editMenu)
        editWidget.layout().addWidget(self.editVersionsMenu)
        editWidget.layout().addWidget(self.newEdit)
        editWidget.layout().addWidget(self.addNewEdit)

        editAssetsWidget = QtGui.QWidget()
        editAssetsWidget.setLayout(QtGui.QHBoxLayout())
        editAssetsWidget.layout().addWidget(self.addGroup)
        editAssetsWidget.layout().addWidget(self.addAsset)
        editAssetsWidget.layout().addWidget(self.update)
        editAssetsWidget.layout().addWidget(self.importEdit)
        editAssetsWidget.layout().addWidget(self.saveEditButton)

        buttonWidget = QtGui.QWidget()
        buttonWidget.setLayout(QtGui.QHBoxLayout())
        buttonWidget.layout().addWidget(self.createAllButton)
        buttonWidget.layout().addWidget(self.createSelectedButton)

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(self.shotWidget)
        self.mainWidget.layout().addWidget(editWidget)
        self.mainWidget.layout().addWidget(self.editTree)
        self.mainWidget.layout().addWidget(editAssetsWidget)
        self.mainWidget.layout().addWidget(buttonWidget)

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Edit (sequence)")

        self.loadEdits()

#        foo = QtGui.QTreeWidgetItem(self.editTree)
#        foo.setText(0, "foo")
#        bar = QtGui.QTreeWidgetItem(self.editTree)
#        bar.setText(0, "bar")

#        testFoo = QtGui.QTreeWidgetItem(foo)
#        testFoo.setText(0, "testFoo")


    def loadEdits(self):
        elements = ueAssetUtils.getElements(self.spec)
        self.editMenu.clear()
        if self.spec.elclass in elements:
            if self.spec.eltype in elements[self.spec.elclass]:
                for name in elements[self.spec.elclass][self.spec.eltype]:
                    self.editMenu.addItem(name)
                self.spec.elname = str(self.editMenu.currentText())
                self.loadEditVersions()

    def loadEditVersions(self):
        versions = ueAssetUtils.getVersions(self.spec)
        self.editVersionsMenu.clear()
        for version in versions:
            self.editVersionsMenu.addItem("%04d" % version["version"])
            self.spec.vers = version["version"]

class Edit(AbstractEdit):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        AbstractEdit.__init__(self, "edit", spec, parent)

        self.setWindowTitle("Edit (sequence)")

        self.parent.edit = ueEdit.getEdit(self.spec)

        for sequence in self.parent.edit["sequences"]:
                sequenceItem = QtGui.QTreeWidgetItem(self.editTree)
                sequenceItem.setText(0, sequence)
                for shot in self.parent.edit[sequence]["shots"]:
                        shotItem = QtGui.QTreeWidgetItem(sequenceItem)
                        shotItem.setText(0, shot)


class Build(AbstractEdit):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        AbstractEdit.__init__(self, "build", spec, parent)

        self.setWindowTitle("Build (libraries)")

	build = ueEdit.getBuild(self.spec)

        for sequence in sorted(build):
            sequenceItem = QtGui.QTreeWidgetItem(self.editTree)
            sequenceItem.setText(0, sequence)
            for shot in sorted(build[sequence]):
                shotItem = QtGui.QTreeWidgetItem(sequenceItem)
                shotItem.setText(0, shot)


class Assets(QtGui.QDockWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec

        self.assetsWidget = QtGui.QTreeWidget()

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(self.assetsWidget)

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Assets")

        for group in ueAssetUtils.getGroupsList(self.spec):
            groupItem = QtGui.QTreeWidgetItem(self.assetsWidget)
            groupItem.setText(0, group)
            self.spec.grp = group
            for asset in ueAssetUtils.getAssetsList(self.spec):
                assetItem = QtGui.QTreeWidgetItem(groupItem)
                assetItem.setText(0, asset)
                self.spec.asst = asset


class AssetInfo(QtGui.QDockWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec

        self.assetsWidget = QtGui.QTableWidget()

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(self.assetsWidget)

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Asset Info")


class Media(QtGui.QDockWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(QtGui.QListWidget())

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Media")


class Spreadsheet(QtGui.QDockWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec

        self.assetTable = QtGui.QTableWidget()
        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(self.assetTable)

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Spreadsheet")

        self.assetTable.insertColumn(0)
        self.assetTable.insertColumn(1)
        self.assetTable.insertColumn(2)
        self.assetTable.insertColumn(3)
        self.assetTable.insertColumn(4)

        for sequence in self.parent.edit["sequences"]:
            for shot in self.parent.edit[sequence]["shots"]:
                asset = self.parent.edit[sequence][shot]
                self.assetTable.insertRow(self.assetTable.rowCount())
                self.assetTable.setItem(self.assetTable.rowCount()-1, 0, QtGui.QTableWidgetItem(shot))
                self.assetTable.setItem(self.assetTable.rowCount()-1, 1, QtGui.QTableWidgetItem(str(asset["startFrame"])))
                self.assetTable.setItem(self.assetTable.rowCount()-1, 2, QtGui.QTableWidgetItem(str(asset["endFrame"])))


class Timeline(QtGui.QDockWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = spec

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setLayout(QtGui.QVBoxLayout())
        self.mainWidget.layout().addWidget(QtGui.QListWidget())

        self.setWidget(self.mainWidget)
        self.setWindowTitle("Timeline")


