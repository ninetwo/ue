import os

from PyQt4 import QtCore, QtGui

import maya.cmds

import ueSpec

import ueMaya
import ueCommon.Render as ueCommonRender

def ueRender():
    Render().show()

class Render(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonRender.setRenderFrom(getRenderLayerList())
        ueCommonRender.setCurrentRender("defaultRenderLayer")

        self.renderWidget = ueCommonRender.Render()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.renderWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueRender [*]")

        self.buttonBox.accepted.connect(self.render)
        self.buttonBox.rejected.connect(self.close)

    def render(self):
        v = ueCommonRender.getValues()
        print v
        self.close()

def getRenderLayerList():
    return maya.cmds.ls(type="renderLayer")

