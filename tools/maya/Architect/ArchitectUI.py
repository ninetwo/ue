import os
import sys
import copy
import random

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec
import ueMaya
import ueCore.AssetUtils as ueAssetUtils
import ueQt.AssetWidgets as ueAssetWidgets

class ArchitectUI(QtGui.QMainWindow):
    def __init__(self, spec=ueSpec.Context().spec, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        self.spec = spec

        self.setWindowTitle("Architect [*]")

        # Actions
        testAction = QtGui.QAction("Test", self)

        # Menubar
        menuBar = QtGui.QMenuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(testAction)

        # Toolbar
        toolBar = QtGui.QToolBar()
        toolBar.addAction(testAction)

        # Central Widget
        centralWidget = QtGui.QWidget()
        foundationsWidget = ArchitectFoundationsWidget(parent=self)
        libraryWidget = ArchitectLibraryWidget(parent=self)

        self.setMenuBar(menuBar)
        self.setCentralWidget(centralWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, foundationsWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, libraryWidget)


class ArchitectFoundationsWidget(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.buildButton = QtGui.QPushButton("Lay Foundation!")

        self.buttons = {"minHeight": ("Min Height", "", QtGui.QSpinBox(), 0),
                        "maxHeight": ("Max Height", "", QtGui.QSpinBox(), 1),
                        "heightBias": ("Height Bias", "", QtGui.QSpinBox(), 2),
                        "deleteVerts": ("Delete Verts", "", QtGui.QCheckBox(), 3)}

        self.foo = QtGui.QWidget()
        self.foo.setLayout(QtGui.QGridLayout())

        self.buildUI()
        self.foo.layout().addWidget(self.buildButton, len(self.buttons), 0, 2, 0)

        self.setWindowTitle("Architect Foundations")
        self.setWidget(self.foo)

        self.buildButton.clicked.connect(self.build)

    def buildUI(self):
        for button in self.buttons:
            button = self.buttons[button]
            self.foo.layout().addWidget(QtGui.QLabel(button[0]), button[3], 0)
            self.foo.layout().addWidget(button[2], button[3], 1)

    def getWidgetsFromUI(self):
        widgets = {}
        for button in self.buttons:
            widgets[button] = self.buttons[button][2]
        return widgets

    def build(self):
        selection = maya.cmds.ls(sl=True)

        if not selection:
            print "Nothing selected"
            return

        widgets = self.getWidgetsFromUI()

        deleteList = []

        # For object in selection
        for s in selection:
            # For face on object
            for face in range(maya.cmds.polyEvaluate(s, f=True)):
                # Extrude our "ground" face inwards to give some space between buildings
                maya.cmds.polyExtrudeFacet("%s.f[%i]"%(s, face), localScale=[0.8, 0.8, 1.0], kft=True)
                edges = self.cleanUp(maya.cmds.polyInfo("%s.f[%i]"%(s, face), faceToEdge=True))
                vertexes = self.cleanUp(maya.cmds.polyInfo("%s.f[%i]"%(s, face), faceToVertex=True))
                if len(edges) > 3:
                    for v in vertexes:
                        vertexEdges = self.cleanUp(maya.cmds.polyInfo("%s.vtx[%i]"%(s, v), vertexToEdge=True))
                        for ve in vertexEdges:
                            if not ve in edges:
                                deleteList.append("%s.e[%i]"%(s, ve))
                # Extrude our building upwards
                maya.cmds.polyExtrudeFacet("%s.f[%i]"%(s, face), localTranslate=[0.0, 0.0, random.uniform(widgets["minHeight"].value(), widgets["maxHeight"].value())], kft=True)

        maya.cmds.delete(*deleteList)

    def cleanUp(self, oldList):
        newList = oldList[0].split()
        del newList[1]
        del newList[0]
        newerList = []
        for n in newList:
            newerList.append(int(n))
        return newerList


class ArchitectLibraryWidget(QtGui.QDockWidget):
    def __init__(self, parent=None):
        QtGui.QDockWidget.__init__(self, parent)

        self.parent = parent
        self.spec = self.parent.spec
        self.elements = []
        self.libraryWidgets = []

        self.shotSelector = ueAssetWidgets.QUeShotListWidget(self.spec)
        self.libraryWidget = QtGui.QWidget()
        self.libraryWidget.setLayout(QtGui.QVBoxLayout())
        self.buildButton = QtGui.QPushButton("Build!")

        self.foo = QtGui.QWidget()
        self.foo.setLayout(QtGui.QVBoxLayout())
        self.foo.layout().setContentsMargins(2, 2, 2, 2)
        self.foo.layout().setSpacing(2)

        self.foo.layout().addWidget(self.shotSelector)
        self.foo.layout().addWidget(self.libraryWidget)
        self.foo.layout().addWidget(self.buildButton)

        self.setWindowTitle("Architect Library")
        self.setWidget(self.foo)

        self.loadElements()

    def loadElements(self):
        self.elements = ueAssetUtils.getElements(self.spec)
        if "arc" in self.elements:
            spec = copy.deepcopy(self.spec)
            spec.elclass = "arc"
            for eltype in self.elements["arc"]:
                spec.eltype = eltype
                self.libraryWidgets.append(LibraryWidget(self.elements["arc"][eltype], parent=self))
            self.drawLibraryWidgets()

    def drawLibraryWidgets(self):
        for widget in self.libraryWidgets:
            self.libraryWidget.layout().addWidget(widget)


class LibraryWidget(QtGui.QWidget):
    def __init__(self, elements, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent
        self.spec = self.parent.spec
        self.elements = elements

        self.libraryList = QtGui.QListWidget()

        self.setLayout(QtGui.QHBoxLayout())

        self.layout().addWidget(QtGui.QLabel(self.spec.eltype))
        self.layout().addWidget(self.libraryList)
        self.drawLibraryElementWidgets()

    def drawLibraryElementWidgets(self):
        for element in self.elements:
            self.libraryList.addItem(element)

