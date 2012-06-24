import os

from PyQt4 import QtCore, QtGui

import ueSpec
import ueCore.AssetUtils as ueAssetUtils

class QUeJobMenu(QtGui.QComboBox):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QComboBox.__init__(self, parent)

        self.spec = spec

        self.loadProjects()

    def loadProjects(self):
        projects = sorted(ueAssetUtils.getProjectsList())
        self.clear()
        self.addItems(projects)
#        if self.spec.proj is not None:
#            self.setCurrentItem(self.item(self.spec.proj))

class QUeGroupMenu(QtGui.QComboBox):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QComboBox.__init__(self, parent)

        self.spec = spec

        self.loadGroups()

    def loadGroups(self):
        groups = sorted(ueAssetUtils.getGroupsList(self.spec))
        self.clear()
        self.addItems(groups)

class QUeAssetMenu(QtGui.QComboBox):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QComboBox.__init__(self, parent)

        self.spec = spec

        self.loadAssets()

    def loadAssets(self):
        assets = sorted(ueAssetUtils.getAssetsList(self.spec))
        self.clear()
        self.addItems(assets)

class QUeShotMenuWidget(QtGui.QWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.spec = spec

        self.jobList = QUeJobMenu(spec)
        self.groupList = QUeGroupMenu(spec)
        self.assetList = QUeAssetMenu(spec)

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.textWidget = QtGui.QWidget()
        self.textWidget.setLayout(QtGui.QHBoxLayout())
        self.textWidget.layout().setContentsMargins(2, 2, 2, 2)
        self.textWidget.layout().setSpacing(2)
        self.textWidget.layout().addWidget(QtGui.QLabel("job"))
        self.textWidget.layout().addWidget(QtGui.QLabel("group"))
        self.textWidget.layout().addWidget(QtGui.QLabel("asset"))

        self.listWidget = QtGui.QWidget()
        self.listWidget.setLayout(QtGui.QHBoxLayout())
        self.listWidget.layout().setContentsMargins(2, 2, 2, 2)
        self.listWidget.layout().setSpacing(2)
        self.listWidget.layout().addWidget(self.jobList)
        self.listWidget.layout().addWidget(self.groupList)
        self.listWidget.layout().addWidget(self.assetList)

        self.layout().addWidget(self.textWidget)
        self.layout().addWidget(self.listWidget)


class QUeJobList(QtGui.QListWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QListWidget.__init__(self, parent)

        self.spec = spec

        self.loadProjects()

    def loadProjects(self):
        projects = sorted(ueAssetUtils.getProjectsList())
        self.clear()
        self.addItems(projects)
#        if self.spec.proj is not None:
#            self.setCurrentItem(self.item(self.spec.proj))

class QUeGroupList(QtGui.QListWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QListWidget.__init__(self, parent)

        self.spec = spec

        self.loadGroups()

    def loadGroups(self):
        groups = sorted(ueAssetUtils.getGroupsList(self.spec))
        self.clear()
        self.addItems(groups)

class QUeAssetList(QtGui.QListWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QListWidget.__init__(self, parent)

        self.spec = spec

        self.loadAssets()

    def loadAssets(self):
        assets = sorted(ueAssetUtils.getAssetsList(self.spec))
        self.clear()
        self.addItems(assets)

class QUeShotListWidget(QtGui.QWidget):
    def __init__(self, spec=ueSpec.Context().spec, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.spec = spec

        self.jobList = QUeJobList(spec)
        self.groupList = QUeGroupList(spec)
        self.assetList = QUeAssetList(spec)

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.textWidget = QtGui.QWidget()
        self.textWidget.setLayout(QtGui.QHBoxLayout())
        self.textWidget.layout().setContentsMargins(2, 2, 2, 2)
        self.textWidget.layout().setSpacing(2)
        self.textWidget.layout().addWidget(QtGui.QLabel("job"))
        self.textWidget.layout().addWidget(QtGui.QLabel("group"))
        self.textWidget.layout().addWidget(QtGui.QLabel("asset"))

        self.listWidget = QtGui.QWidget()
        self.listWidget.setLayout(QtGui.QHBoxLayout())
        self.listWidget.layout().setContentsMargins(2, 2, 2, 2)
        self.listWidget.layout().setSpacing(2)
        self.listWidget.layout().addWidget(self.jobList)
        self.listWidget.layout().addWidget(self.groupList)
        self.listWidget.layout().addWidget(self.assetList)

        self.layout().addWidget(self.textWidget)
        self.layout().addWidget(self.listWidget)

