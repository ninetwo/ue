import os, sys

import glob

from PyQt4 import QtCore, QtGui

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname
global comment, thumbnail

global elclasses
elclasses = []

def getValues():
    dbMeta = {}
    if not comment == None:
        dbMeta["comment"] = comment
    if not thumbnail == None:
        dbMeta["thumbnail"] = thumbnail
    return ueSpec.Spec(proj, grp, asst, elclass, eltype, elname), dbMeta

def setClasses(classes):
    global elclasses
    elclasses = classes

class Save(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname
        global comment, thumbnail

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
        asst = os.getenv("ASST")
        elclass = None
        eltype = None
        elname = None
        comment = None
        thumbnail = None

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

        self.thumbnailBox.setFixedHeight(160)

        pl = sorted(ueAssetUtils.getProjectsList())
        for p in pl:
            self.projMenu.addItem(p)
        self.projMenu.setCurrentIndex(pl.index(proj))

        gl = sorted(ueAssetUtils.getGroupsList(ueSpec.Spec(proj)))
        for g in gl:
            self.grpMenu.addItem(g)
        self.grpMenu.setCurrentIndex(gl.index(grp))

        al = sorted(ueAssetUtils.getAssetsList(ueSpec.Spec(proj, grp)))
        for a in al:
            self.asstMenu.addItem(a)
        self.asstMenu.setCurrentIndex(al.index(asst))

        for c in sorted(self.elclasses):
            self.elclassMenu.addItem(c)
        elclass = str(self.elclassMenu.currentText())

        self.elements = ueAssetUtils.getElements(ueSpec.Spec(proj, grp, asst))

        if elclass in sorted(self.elements):
            for t in self.elements[elclass]:
                self.eltypeMenu.addItem(t)
            eltype = str(self.eltypeMenu.currentText())

            if eltype in self.elements[elclass]:
                for n in sorted(self.elements[elclass][eltype]):
                    self.elnameMenu.addItem(n)
                elname = str(self.elnameMenu.currentText())

        t = QtGui.QWidget()
        t.setLayout(QtGui.QHBoxLayout())

        self.thumbnailButtons = []
        for f in glob.glob(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")):
            w = QtGui.QWidget()
            w.setLayout(QtGui.QVBoxLayout())

            name = os.path.basename(f).lstrip("ueSaveThumbs_").rstrip(".png")

            label = QtGui.QLabel()
            img = QtGui.QImage(f)
            imgs = img.scaled(250, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            label.setPixmap(QtGui.QPixmap.fromImage(imgs))
            radio = QtGui.QRadioButton(name)

            self.thumbnailButtons.append(radio)

            radio.toggled.connect(self.loadThumbnail)

            w.layout().addWidget(label)
            w.layout().addWidget(radio)

            t.layout().addWidget(w)

        self.thumbnailBox.setWidget(t)

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
        self.elnameMenu.activated.connect(self.setName)
        self.eltypeBox.textEdited.connect(self.newType)
        self.elnameBox.textEdited.connect(self.newName)
        self.commentBox.textChanged.connect(self.loadComment)

    def loadProjects(self):
        pl = sorted(ueAssetUtils.getProjectsList())
        self.projMenu.clear()
        for p in pl:
            self.projMenu.addItem(p)
        self.loadGroups()

    def loadGroups(self):
        global proj
        proj = str(self.projMenu.currentText())
        spec = ueSpec.Spec(proj)
        gl = sorted(ueAssetUtils.getGroupsList(spec))
        self.grpMenu.clear()
        for g in gl:
            self.grpMenu.addItem(g)
        self.loadAssets()

    def loadAssets(self):
        global grp
        grp = str(self.grpMenu.currentText())
        spec = ueSpec.Spec(proj, grp)
        al = sorted(ueAssetUtils.getAssetsList(spec))
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
        for e in sorted(self.elclasses):
            self.elclassMenu.addItem(e)
        self.loadTypes()

    def loadTypes(self):
        global elclass
        elclass = str(self.elclassMenu.currentText())
        self.eltypeMenu.clear()
        if elclass in self.elements:
            for t in sorted(self.elements[elclass]):
                self.eltypeMenu.addItem(t)
            self.loadNames()
        else:
            self.elnameMenu.clear()

    def loadNames(self):
        global eltype, elname
        eltype = str(self.eltypeMenu.currentText())
        self.elnameMenu.clear()
        if eltype in self.elements[elclass]:
            for n in sorted(self.elements[elclass][eltype]):
                self.elnameMenu.addItem(n)
            elname = str(self.elnameMenu.currentText())

    def setName(self):
        global elname
        elname = str(self.elnameMenu.currentText())

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

    def loadComment(self):
        global comment
        comment = str(self.commentBox.toPlainText())

    def loadThumbnail(self):
        global thumbnail
        for t in self.thumbnailButtons:
            if t.isChecked():
                thumbnail = t.text()

#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv) 
#    win = Save()
#    win.show()
#    sys.exit(app.exec_())

