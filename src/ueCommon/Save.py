import os, sys

from PyQt4 import QtCore, QtGui

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname

global elclasses
elclasses = []

def getValues():
    return (proj, grp, asst, elclass, eltype, elname)

def setClasses(classes):
    global elclasses
    elclasses = classes

class Save(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GROUP")
        asst = os.getenv("ASST")
        elclass = None
        eltype = None
        elname = None

        self.setLayout(QtGui.QGridLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.projMenu = QtGui.QComboBox()
        self.grpMenu = QtGui.QComboBox()
        self.asstMenu = QtGui.QComboBox()
        self.elclassMenu = QtGui.QComboBox()
        self.eltypeMenu = QtGui.QComboBox()
        self.eltypeBox = QtGui.QLineEdit()
        self.elnameMenu = QtGui.QComboBox()
        self.elnameBox = QtGui.QLineEdit()

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
                self.eltypeMenu.addItem(t)
            eltype = str(self.eltypeMenu.currentText())

            if eltype in self.elements[elclass]:
                for n in self.elements[elclass][eltype]:
                    self.elnameMenu.addItem(n)
                elname = str(self.elnameMenu.currentText())

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
        two.setLayout(QtGui.QGridLayout())

        two.layout().addWidget(QtGui.QLabel("Class"), 0, 0)
        two.layout().addWidget(self.elclassMenu, 0, 1)
        two.layout().addWidget(QtGui.QLabel("Type"), 1, 0)
        two.layout().addWidget(self.eltypeMenu, 1, 1)
        two.layout().addWidget(self.eltypeBox, 1, 2)
        two.layout().addWidget(QtGui.QLabel("Name"), 2, 0)
        two.layout().addWidget(self.elnameMenu, 2, 1)
        two.layout().addWidget(self.elnameBox, 2, 2)

        self.layout().addWidget(one)
        self.layout().addWidget(two)

        self.projMenu.activated.connect(self.loadGroups)
        self.grpMenu.activated.connect(self.loadAssets)
        self.asstMenu.activated.connect(self.loadElements)
        self.elclassMenu.activated.connect(self.loadTypes)
        self.eltypeMenu.activated.connect(self.loadNames)
        self.eltypeBox.textEdited.connect(self.newType)
        self.elnameBox.textEdited.connect(self.newName)

    def newType(self):
        global eltype
        if str(self.eltypeBox.text()) == "":
            eltype = str(self.eltypeMenu.currentText())
        else:
            eltype = str(self.eltypeBox.text())

    def newName(self):
        global elname
        if str(self.elnameBox.text()) == "":
            elname = str(self.elnameMenu.currentText())
        else:
            elname = str(self.elnameBox.text())

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
        if elclass in self.elements:
            self.loadTypes()
        else:
            self.eltypeMenu.clear()
            self.elnameMenu.clear()

    def loadTypes(self):
        global elclass
        elclass = str(self.elclassMenu.currentText())
        self.eltypeMenu.clear()
        if elclass in self.elements:
            for t in self.elements[elclass]:
                self.eltypeMenu.addItem(t)
            self.loadNames()
        else:
            self.elnameMenu.clear()

    def loadNames(self):
        global eltype, elname
        eltype = str(self.eltypeMenu.currentText())
        self.elnameMenu.clear()
        if eltype in self.elements[elclass]:
            for n in self.elements[elclass][eltype]:
                self.elnameMenu.addItem(n)
            elname = str(self.elnameMenu.currentText())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv) 
    win = Save()
    win.show()
    sys.exit(app.exec_())

