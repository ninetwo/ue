import os, sys, glob

from PyQt4 import QtCore, QtGui

import ueSpec

import ueCore
import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst, elclass, eltype, elname, vers, elpass

global elclasses
elclasses = []

def getValues():
    return ueSpec.Spec(proj, grp, asst,
                       elclass, eltype, elname,
                       vers, elpass)

def setClasses(classes):
    global elclasses
    elclasses = classes

class Open(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        global proj, grp, asst, elclass, eltype, elname, vers, elpass

        self.elclasses = elclasses

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
        asst = os.getenv("ASST")
        elclass = None
        eltype = None
        elname = None
        vers = None
        elpass = None

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

        self.passList = QtGui.QListWidget()

        self.elCreatedBy = QtGui.QLabel("N/A")
        self.elCreatedAt = QtGui.QLabel("N/A")
        self.elComment = QtGui.QLabel("N/A")
        self.elThumb = QtGui.QLabel()

        self.verCreatedBy = QtGui.QLabel("N/A")
        self.verCreatedAt = QtGui.QLabel("N/A")
        self.verComment = QtGui.QLabel("N/A")
        self.verThumb = QtGui.QLabel()
        self.verFilesList = QtGui.QListWidget()

        img = QtGui.QImage(os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png"))
        imgs = img.scaled(200, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        self.elThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))
        self.verThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))

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

        if elclass in self.elements:
            for t in sorted(self.elements[elclass]):
                self.eltypeList.addItem(QtGui.QListWidgetItem(t))
            self.eltypeList.setCurrentItem(self.eltypeList.item(0))
            eltype = str(self.eltypeList.currentItem().text())

            if eltype in self.elements[elclass]:
                for n in sorted(self.elements[elclass][eltype]):
                    self.elnameList.addItem(QtGui.QListWidgetItem(n))
                self.elnameList.setCurrentItem(self.elnameList.item(0))
                elname = str(self.elnameList.currentItem().text())

                self.updateElInfo()

                self.versions = ueAssetUtils.getVersions(ueSpec.Spec(proj, grp, asst,
                                                         elclass, eltype, elname))
                if len(self.versions) > 0:
                    for v in sorted(range(len(self.versions)), reverse=True):
                        self.versList.addItem(QtGui.QListWidgetItem("%04d" % int(v+1)))
                    self.versList.setCurrentItem(self.versList.item(0))
                    vers = int(self.versList.currentItem().text())

                    self.loadPasses()

                    self.updateVersInfo()

        asstBox = QtGui.QGroupBox("Asset")
        asstBox.setLayout(QtGui.QHBoxLayout())

        asstBox.layout().addWidget(QtGui.QLabel("Project"))
        asstBox.layout().addWidget(self.projMenu)
        asstBox.layout().addWidget(QtGui.QLabel("Group"))
        asstBox.layout().addWidget(self.grpMenu)
        asstBox.layout().addWidget(QtGui.QLabel("Asset"))
        asstBox.layout().addWidget(self.asstMenu)
        asstBox.layout().addStretch(0)

        passBox = QtGui.QGroupBox("Pass")
        passBox.setLayout(QtGui.QHBoxLayout())

        passBox.layout().addWidget(self.passList)

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

        elInfoBox = QtGui.QGroupBox("Element Info")
        elInfoBox.setLayout(QtGui.QGridLayout())

        elInfoBox.layout().addWidget(QtGui.QLabel("Created by"), 0, 0)
        elInfoBox.layout().addWidget(self.elCreatedBy, 0, 1)
        elInfoBox.layout().addWidget(QtGui.QLabel("Created at"), 1, 0)
        elInfoBox.layout().addWidget(self.elCreatedAt, 1, 1)
        elInfoBox.layout().addWidget(QtGui.QLabel("Comment"),2, 0)
        elInfoBox.layout().addWidget(self.elComment, 2, 1)
        elInfoBox.layout().addWidget(self.elThumb, 0, 2, 3, 2)

        verInfoBox = QtGui.QGroupBox("Version Info")
        verInfoBox.setLayout(QtGui.QGridLayout())

        verInfoBox.layout().addWidget(QtGui.QLabel("Created by"), 0, 0)
        verInfoBox.layout().addWidget(self.verCreatedBy, 0, 1)
        verInfoBox.layout().addWidget(QtGui.QLabel("Created at"), 1, 0)
        verInfoBox.layout().addWidget(self.verCreatedAt, 1, 1)
        verInfoBox.layout().addWidget(QtGui.QLabel("Comment"),2, 0)
        verInfoBox.layout().addWidget(self.verComment, 2, 1)
        verInfoBox.layout().addWidget(QtGui.QLabel("Files"), 3, 0, 1, 4)
        verInfoBox.layout().addWidget(self.verFilesList, 4, 0, 1, 4)
        verInfoBox.layout().addWidget(self.verThumb, 0, 2, 3, 2)

        self.layout().addWidget(asstBox)
        self.layout().addWidget(elBox)
        self.layout().addWidget(passBox)
        self.layout().addWidget(elInfoBox)
        self.layout().addWidget(verInfoBox)

        self.projMenu.activated.connect(self.loadGroups)
        self.grpMenu.activated.connect(self.loadAssets)
        self.asstMenu.activated.connect(self.loadElements)
        self.elclassMenu.activated.connect(self.loadTypes)
        self.eltypeList.itemSelectionChanged.connect(self.loadNames)
        self.elnameList.itemSelectionChanged.connect(self.loadVers)
        self.versList.itemSelectionChanged.connect(self.setVers)
        self.passList.itemSelectionChanged.connect(self.setPass)

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
#        self.eltypeList.clear()
        self.loadTypes()

    def loadTypes(self):
        global elclass
        elclass = str(self.elclassMenu.currentText())
        self.eltypeList.clear()
        if elclass in self.elements:
            for t in sorted(self.elements[elclass]):
                self.eltypeList.addItem(QtGui.QListWidgetItem(t))
            self.eltypeList.setCurrentItem(self.eltypeList.item(0))
#            self.loadNames()
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
#                self.loadVers()
            else:
                self.versList.clear()

    def loadVers(self):
        global elname, vers
        elname = str(self.elnameList.currentItem().text())
        spec = ueSpec.Spec(proj, grp, asst, elclass, eltype, elname)
        self.versions = ueAssetUtils.getVersions(spec)
        self.versList.clear()
        if len(self.versions) > 0:
            for v in sorted(range(len(self.versions)), reverse=True):
                self.versList.addItem(QtGui.QListWidgetItem("%04d" % int(v+1)))
            self.versList.setCurrentItem(self.versList.item(0))
            vers = str(self.versList.currentItem().text())
        else:
            vers = None
        self.loadPasses()
        self.updateElInfo()

    def setVers(self):
        global vers
        vers = int(self.versList.currentItem().text())
        self.loadPasses()
        self.updateVersInfo()

    def loadPasses(self):
        global elpass
        self.passList.clear()
        if int(vers)-1 <= len(self.versions):
            if "passes" in self.versions[int(vers)-1]:
                for p in self.versions[int(vers)-1]["passes"].split(","):
                    self.passList.addItem(QtGui.QListWidgetItem(p))
                self.passList.setCurrentItem(self.passList.item(0))
                elpass = str(self.passList.currentItem().text())
            else:
                elpass = None
        else:
            elpass = None

    def setPass(self):
        global elpass
        elpass = str(self.passList.currentItem().text())
        self.updateVersInfo()

    def updateElInfo(self):
        try:
            el = self.elements[elclass][eltype][elname]
            self.elCreatedBy.setText(el["created_by"])
            self.elCreatedAt.setText(ueCore.formatDatetime(el["created_at"]))
            if "comment" in el:
                self.elComment.setText(el["comment"])
            else:
                self.elComment.setText("N/A")
            if "thumbnail" in el:
                spec = ueSpec.Spec(proj, grp, asst, elclass, eltype, elname)
                f = ueAssetUtils.getThumbnailPath(spec)
                img = QtGui.QImage(f)
                imgs = img.scaled(200, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.elThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))
            else:
                img = QtGui.QImage(os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png"))
                imgs = img.scaled(200, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.elThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))
        except KeyError:
            pass

    def updateVersInfo(self):
        try:
            ver = self.versions[int(vers)-1]
            spec = ueSpec.Spec(proj, grp, asst, elclass, eltype, elname, vers, elpass)

            self.verCreatedBy.setText(ver["created_by"])
            self.verCreatedAt.setText(ueCore.formatDatetime(ver["created_at"]))

            files = glob.glob(os.path.join(ueAssetUtils.getVersionPath(spec), ueAssetUtils.getElementName(spec)+"*"))
            self.verFilesList.clear()
            for f in sorted(files):
                self.verFilesList.addItem(QtGui.QListWidgetItem(os.path.basename(f)))

            if "comment" in ver:
                self.verComment.setText(ver["comment"])
            else:
                self.verComment.setText("N/A")

            if "thumbnail" in ver:
                spec = ueSpec.Spec(proj, grp, asst, elclass, eltype, elname, vers)
                f = ueAssetUtils.getThumbnailPath(spec)
                img = QtGui.QImage(f)
                imgs = img.scaled(200, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.verThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))
            else:
                img = QtGui.QImage(os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png"))
                imgs = img.scaled(200, 80, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
                self.verThumb.setPixmap(QtGui.QPixmap.fromImage(imgs))
        except IndexError:
            pass

#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    win = Open()
#    win.show()
#    sys.exit(app.exec_())

