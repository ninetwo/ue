import os, sys

import glob

from PyQt4 import QtCore, QtGui

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname

global elclasses
elclasses = []

def getValues():
    return ueSpec.Spec(proj, grp, asst, elclass, eltype, elname)

def setClasses(classes):
    global elclasses
    elclasses = classes

class Save(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
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
        self.commentBox = QtGui.QTextEdit()
        self.thumbnailBox = QtGui.QScrollArea()

        self.thumbnailBox.setFixedHeight(140)

        labs = []
        for f in glob.glob(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")):
            lab = QtGui.QLabel()
            img = QtGui.QImage(f)
            imgs = img.scaled(250, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            lab.setPixmap(QtGui.QPixmap.fromImage(imgs))
            labs.append(lab)

        t = QtGui.QWidget()
        t.setLayout(QtGui.QGridLayout())

        for l in labs:
            i = labs.index(l)
            t.layout().addWidget(l, 0, i)
            t.layout().addWidget(QtGui.QRadioButton(), 1, i)

        self.thumbnailBox.setWidget(t)

        pl = ueAssetUtils.getProjectsList()
        for p in pl:
            self.projMenu.addItem(p)
        self.projMenu.setCurrentIndex(pl.index(proj))

        gl = ueAssetUtils.getGroupsList(ueSpec.Spec(proj))
        for g in gl:
            self.grpMenu.addItem(g)
        self.grpMenu.setCurrentIndex(gl.index(grp))

        al = ueAssetUtils.getAssetsList(ueSpec.Spec(proj, grp))
        for a in al:
            self.asstMenu.addItem(a)
        self.asstMenu.setCurrentIndex(al.index(asst))

        for c in self.elclasses:
            self.elclassMenu.addItem(c)
        elclass = str(self.elclassMenu.currentText())

        self.elements = ueAssetUtils.getElements(ueSpec.Spec(proj, grp, asst))

        if elclass in self.elements:
            for t in self.elements[elclass]:
                self.eltypeMenu.addItem(t)
            eltype = str(self.eltypeMenu.currentText())

            if eltype in self.elements[elclass]:
                for n in self.elements[elclass][eltype]:
                    self.elnameMenu.addItem(n)
                elname = str(self.elnameMenu.currentText())

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
        elBox.setLayout(QtGui.QGridLayout())

        elBox.layout().addWidget(QtGui.QLabel("Class"), 0, 0)
        elBox.layout().addWidget(self.elclassMenu, 0, 1)
        elBox.layout().addWidget(QtGui.QLabel("Type"), 1, 0)
        elBox.layout().addWidget(self.eltypeMenu, 1, 1)
        elBox.layout().addWidget(self.eltypeBox, 1, 2)
        elBox.layout().addWidget(QtGui.QLabel("Name"), 2, 0)
        elBox.layout().addWidget(self.elnameMenu, 2, 1)
        elBox.layout().addWidget(self.elnameBox, 2, 2)

        miscBox = QtGui.QGroupBox("Optional")
        miscBox.setLayout(QtGui.QVBoxLayout())

        miscBox.layout().addWidget(QtGui.QLabel("Thumbnail"))
        miscBox.layout().addWidget(self.thumbnailBox)
        miscBox.layout().addWidget(QtGui.QLabel("Comment"))
        miscBox.layout().addWidget(self.commentBox)

        self.layout().addWidget(asstBox)
        self.layout().addWidget(elBox)
        self.layout().addWidget(miscBox)

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
        spec = ueSpec.Spec(proj)
        gl = ueAssetUtils.getGroupsList(spec)
        self.grpMenu.clear()
        for g in gl:
            self.grpMenu.addItem(g)
        self.loadAssets()

    def loadAssets(self):
        global grp
        grp = str(self.grpMenu.currentText())
        spec = ueSpec.Spec(proj, grp)
        al = ueAssetUtils.getAssetsList(spec)
        self.asstMenu.clear()
        for a in al:
            self.asstMenu.addItem(a)
        self.loadElements()

    def loadElements(self):
        global asst
        asst = str(self.asstMenu.currentText())
        spec = ueSpec.Spec(proj, grp, asst)
        self.elements = ueAssetUtils.getElements(spec)
        if elclass in self.elements:
            self.loadTypes()
        else:
            self.eltypeMenu.clear()
            self.elnameMenu.clear()

    def loadClasses(self):
        global elclass
        elclass = self.elclasses[0]
        self.elclassMenu.clear()
        for e in self.elclasses:
            self.elclassMenu.addItem(e)
        self.loadTypes()

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

