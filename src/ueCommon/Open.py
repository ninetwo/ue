import os, sys

from PyQt4 import QtCore, QtGui

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname, vers

global elclasses
elclasses = []

def getValues():
    return (proj, grp, asst, elclass, eltype, elname, vers)

def setClasses(classes):
    global elclasses
    elclasses = classes

class Open(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname, vers

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GROUP")
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

        pl = ueAssetUtils.getProjectsList()
        for p in pl:
            self.projMenu.addItem(p)
        self.projMenu.setCurrentIndex(pl.index(proj))

        gl = ueAssetUtils.getGroupsList(proj)
        for g in gl:
            self.grpMenu.addItem(g)
        self.grpMenu.setCurrentIndex(gl.index(grp))

        al = ueAssetUtils.getAssetsList(proj, grp)
        for a in al:
            self.asstMenu.addItem(a)
        self.asstMenu.setCurrentIndex(al.index(asst))

        for c in self.elclasses:
            self.elclassMenu.addItem(c)
        elclass = str(self.elclassMenu.currentText())

        self.elements = ueAssetUtils.getElements(proj, grp, asst)

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

                versions = ueAssetUtils.getVersions(proj, grp, asst,
                                                    elclass, eltype, elname)
                for v in sorted(range(len(versions)), reverse=True):
                    self.versList.addItem(QtGui.QListWidgetItem("%03d" % int(v+1)))
                self.versList.setCurrentItem(self.versList.item(0))
                vers = int(self.versList.currentItem().text())

        one = QtGui.QWidget()
        one.setLayout(QtGui.QHBoxLayout())

        one.layout().addWidget(QtGui.QLabel("Project"))
        one.layout().addWidget(self.projMenu)
        one.layout().addWidget(QtGui.QLabel("Group"))
        one.layout().addWidget(self.grpMenu)
        one.layout().addWidget(QtGui.QLabel("Asset"))
        one.layout().addWidget(self.asstMenu)
        one.layout().addStretch(0)

        two = QtGui.QWidget()
        two.setLayout(QtGui.QHBoxLayout())

        twoa = QtGui.QWidget()
        twoa.setLayout(QtGui.QVBoxLayout())

        twoa.layout().addWidget(QtGui.QLabel("Class"))
        twoa.layout().addWidget(self.elclassMenu)
        twoa.layout().addWidget(QtGui.QLabel("Type"))
        twoa.layout().addWidget(self.eltypeList)
        twoa.layout().addWidget(QtGui.QLabel("Name"))
        twoa.layout().addWidget(self.elnameList)

        twob = QtGui.QWidget()
        twob.setLayout(QtGui.QVBoxLayout())

        twob.layout().addWidget(QtGui.QLabel("Version"))
        twob.layout().addWidget(self.versList)

        two.layout().addWidget(twoa)
        two.layout().addWidget(twob)

        self.layout().addWidget(one)
        self.layout().addWidget(two)

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
        for p in pl:
            self.projMenu.addItem(p)
        self.loadGroups()

    def loadGroups(self):
        global proj
        proj = str(self.projMenu.currentText())
        gl = ueAssetUtils.getGroupsList(proj)
        self.grpMenu.clear()
        for g in gl:
            self.grpMenu.addItem(g)
        self.loadAssets()

    def loadAssets(self):
        global grp
        grp = str(self.grpMenu.currentText())
        al = ueAssetUtils.getAssetsList(proj, grp)
        self.asstMenu.clear()
        for a in al:
            self.asstMenu.addItem(a)
        self.loadElements()

    def loadElements(self):
        global asst
        asst = str(self.asstMenu.currentText())
        self.elements = ueAssetUtils.getElements(proj, grp, asst)
        self.eltypeList.clear()

    def loadTypes(self):
        global elclass
        elclass = str(self.elclassMenu.currentText())
        self.eltypeList.clear()
        if elclass in self.elements:
            for t in self.elements[elclass]:
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
                for n in self.elements[elclass][eltype]:
                    self.elnameList.addItem(QtGui.QListWidgetItem(n))
                self.elnameList.setCurrentItem(self.elnameList.item(0))
                self.loadVers()
            else:
                self.versList.clear()

    def loadVers(self):
        global elname, vers
        elname = str(self.elnameList.currentItem().text())
        self.versList.clear()
        versions = ueAssetUtils.getVersions(proj, grp, asst,
                                            elclass, eltype, elname)
        if len(versions) > 0:
            for v in sorted(range(len(versions)), reverse=True):
                self.versList.addItem(QtGui.QListWidgetItem("%03d" % int(v+1)))
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

