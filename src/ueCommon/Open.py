import os, sys

from PyQt4 import QtCore, QtGui

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname, vers

global elclasses
elclasses = []

def getValues():
    return ueSpec.Spec(proj, grp, asst,
                       elclass, eltype, elname, vers)

def setClasses(classes):
    global elclasses
    elclasses = classes

class Open(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname, vers

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
        asst = os.getenv("ASST")
        elclass = None
        eltype = None
        elname = None
        vers = None

        self.setLayout(QtGui.QGridLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.projMenu = QtGui.QComboBox()
        self.grpMenu = QtGui.QComboBox()
        self.asstMenu = QtGui.QComboBox()
        self.elclassMenu = QtGui.QComboBox()
        self.eltypeList = QtGui.QListWidget()
        self.elnameList = QtGui.QListWidget()
        self.versList = QtGui.QListWidget()
        self.createUser = QtGui.QLabel("N/A")
        self.createTime = QtGui.QLabel("N/A")
        self.metadata = QtGui.QLabel("N/A")
        self.filesList = QtGui.QListWidget()

        pl = ueAssetUtils.getProjectsList()
        for p in sorted(pl):
            self.projMenu.addItem(p)
        self.projMenu.setCurrentIndex(pl.index(proj))

        gl = ueAssetUtils.getGroupsList(ueSpec.Spec(proj))
        for g in sorted(gl):
            self.grpMenu.addItem(g)
        self.grpMenu.setCurrentIndex(gl.index(grp))

        al = ueAssetUtils.getAssetsList(ueSpec.Spec(proj, grp))
        for a in sorted(al):
            self.asstMenu.addItem(a)
        self.asstMenu.setCurrentIndex(al.index(asst))

        for c in sorted(self.elclasses):
            self.elclassMenu.addItem(c)
        elclass = str(self.elclassMenu.currentText())

        self.elements = ueAssetUtils.getElements(ueSpec.Spec(proj, grp, asst))

        if elclass in self.elements:
            for t in self.elements[elclass]:
                self.eltypeList.addItem(QtGui.QListWidgetItem(t))
            self.eltypeList.setCurrentItem(self.eltypeList.item(0))
            eltype = str(self.eltypeList.currentItem().text())

            if eltype in self.elements[elclass]:
                for n in self.elements[elclass][eltype]:
                    self.elnameList.addItem(QtGui.QListWidgetItem(n))
                self.elnameList.setCurrentItem(self.elnameList.item(0))
                elname = str(self.elnameList.currentItem().text())

                versions = ueAssetUtils.getVersions(ueSpec.Spec(proj, grp, asst,
                                                    elclass, eltype, elname))
                for v in sorted(range(len(versions)), reverse=True):
                    self.versList.addItem(QtGui.QListWidgetItem("%04d" % int(v+1)))
                self.versList.setCurrentItem(self.versList.item(0))
                vers = int(self.versList.currentItem().text())

        asstBox = QtGui.QGroupBox("Asset")
        asstBox.setLayout(QtGui.QHBoxLayout())

        asstBox.layout().addWidget(QtGui.QLabel("Project"))
        asstBox.layout().addWidget(self.projMenu)
        asstBox.layout().addWidget(QtGui.QLabel("Group"))
        asstBox.layout().addWidget(self.grpMenu)
        asstBox.layout().addWidget(QtGui.QLabel("Asset"))
        asstBox.layout().addWidget(self.asstMenu)
        asstBox.layout().addStretch(0)

        elBox = QtGui.QGroupBox("Element")
        elBox.setLayout(QtGui.QHBoxLayout())

        elDesc = QtGui.QWidget()
        elDesc.setLayout(QtGui.QVBoxLayout())

        elDesc.layout().addWidget(QtGui.QLabel("Class"))
        elDesc.layout().addWidget(self.elclassMenu)
        elDesc.layout().addWidget(QtGui.QLabel("Type"))
        elDesc.layout().addWidget(self.eltypeList)
        elDesc.layout().addWidget(QtGui.QLabel("Name"))
        elDesc.layout().addWidget(self.elnameList)

        elVers = QtGui.QWidget()
        elVers.setLayout(QtGui.QVBoxLayout())

        elVers.layout().addWidget(QtGui.QLabel("Version"))
        elVers.layout().addWidget(self.versList)

        elBox.layout().addWidget(elDesc)
        elBox.layout().addWidget(elVers)

        infoBox = QtGui.QGroupBox("Element Info")
        infoBox.setLayout(QtGui.QGridLayout())

        infoBox.layout().addWidget(QtGui.QLabel("Created by:"), 0, 0)
        infoBox.layout().addWidget(self.createUser, 0, 1)
        infoBox.layout().addWidget(QtGui.QLabel("Created at:"), 1, 0)
        infoBox.layout().addWidget(self.createTime, 1, 1)
        infoBox.layout().addWidget(QtGui.QLabel("Metadata:"), 2, 0)
        infoBox.layout().addWidget(self.metadata, 2, 1)
        infoBox.layout().addWidget(QtGui.QLabel("Files"), 0, 2)
        infoBox.layout().addWidget(self.filesList, 1, 2, 2, 1)

        self.layout().addWidget(asstBox)
        self.layout().addWidget(elBox)
        self.layout().addWidget(infoBox)

        self.projMenu.activated.connect(self.loadGroups)
        self.grpMenu.activated.connect(self.loadAssets)
        self.asstMenu.activated.connect(self.loadElements)
        self.elclassMenu.activated.connect(self.loadTypes)
        self.eltypeList.itemSelectionChanged.connect(self.loadNames)
        self.elnameList.itemSelectionChanged.connect(self.loadVers)
        self.versList.itemSelectionChanged.connect(self.setVers)

    def loadProjects(self):
        pl = ueAssetUtils.getProjectsList()
        self.projMenu.clear()
        for p in sorted(pl):
            self.projMenu.addItem(p)
        self.loadGroups()

    def loadGroups(self):
        global proj
        proj = str(self.projMenu.currentText())
        spec = ueSpec.Spec(proj)
        gl = ueAssetUtils.getGroupsList(spec)
        self.grpMenu.clear()
        for g in sorted(gl):
            self.grpMenu.addItem(g)
        self.loadAssets()

    def loadAssets(self):
        global grp
        grp = str(self.grpMenu.currentText())
        spec = ueSpec.Spec(proj, grp)
        al = ueAssetUtils.getAssetsList(spec)
        self.asstMenu.clear()
        for a in sorted(al):
            self.asstMenu.addItem(a)
        self.loadElements()

    def loadElements(self):
        global asst
        asst = str(self.asstMenu.currentText())
        spec = ueSpec.Spec(proj, grp, asst)
        self.elements = ueAssetUtils.getElements(spec)
        self.eltypeList.clear()

    def loadTypes(self):
        global elclass
        elclass = str(self.elclassMenu.currentText())
        self.eltypeList.clear()
        if elclass in self.elements:
            for t in sorted(self.elements[elclass]):
                self.eltypeList.addItem(QtGui.QListWidgetItem(t))
            self.eltypeList.setCurrentItem(self.eltypeList.item(0))
            self.loadNames()
        else:
            self.elnameList.clear()
            self.versList.clear()

    def loadNames(self):
        global eltype
        eltype = str(self.eltypeList.currentItem().text())
        self.elnameList.clear()
        if elclass in self.elements:
            if eltype in self.elements[elclass]:
                for n in sorted(self.elements[elclass][eltype]):
                    self.elnameList.addItem(QtGui.QListWidgetItem(n))
                self.elnameList.setCurrentItem(self.elnameList.item(0))
                self.loadVers()
            else:
                self.versList.clear()

    def loadVers(self):
        global elname, vers
        elname = str(self.elnameList.currentItem().text())
        spec = ueSpec.Spec(proj, grp, asst, elclass, eltype, elname)
        versions = ueAssetUtils.getVersions(spec)
        self.versList.clear()
        if len(versions) > 0:
            for v in sorted(range(len(versions)), reverse=True):
                self.versList.addItem(QtGui.QListWidgetItem("%04d" % int(v+1)))
            self.versList.setCurrentItem(self.versList.item(0))
            vers = int(self.versList.item(0).text())
        else:
            vers = None

    def setVers(self):
        global vers
        vers = str(self.versList.currentItem().text())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = Open()
    win.show()
    sys.exit(app.exec_())

