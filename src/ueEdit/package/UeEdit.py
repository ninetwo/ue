import os

from rv import rvtypes, commands

from PyQt4 import QtGui, QtCore

import ueClient
import ueSpec

import ueEdit
from ueEdit import EditUI as ueEditUI

class UeEdit(rvtypes.MinorMode):
    def __init__(self, mainWindow=None):
        rvtypes.MinorMode.__init__(self)

        self.mainWindow = mainWindow

        if self.mainWindow is None:
            return

        ueClient.Client()

        self.spec = ueSpec.Context().spec
        self.edit = {"sequences": []}

        self.toolBox = ueEditUI.ToolBox(parent=self.mainWindow)
        self.edit = ueEditUI.Edit(spec=self.spec, parent=self.mainWindow)
        self.build = ueEditUI.Build(spec=self.spec, parent=self.mainWindow)
        self.assets = ueEditUI.Assets(spec=self.spec, parent=self.mainWindow)
        self.media = ueEditUI.Media(spec=self.spec, parent=self.mainWindow)
        self.assetInfo = ueEditUI.AssetInfo(spec=self.spec, parent=self.mainWindow)
        self.spreadsheet = ueEditUI.Spreadsheet(spec=self.spec, parent=self.mainWindow)
        self.timeline = ueEditUI.Timeline(spec=self.spec, parent=self.mainWindow)

        self.mainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBox)
        self.mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.edit)
        self.mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.build)
        self.mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.assets)
        self.mainWindow.tabifyDockWidget(self.build, self.edit)
        self.mainWindow.tabifyDockWidget(self.edit, self.assets)
        self.mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.media)
        self.mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.assetInfo)
        self.mainWindow.tabifyDockWidget(self.media, self.assetInfo)
        self.mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.spreadsheet)
        self.mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.timeline)
        self.mainWindow.tabifyDockWidget(self.spreadsheet, self.timeline)


def createMode():
    widgets = QtGui.QApplication.allWidgets()
    for widget in widgets:
        if str(type(widget)) == "<class 'PyQt4.QtGui.QMainWindow'>":
            return UeEdit(widget)
    return UeEdit()

