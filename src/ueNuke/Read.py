import sys, os

from PyQt4 import QtCore, QtGui

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

import ueNuke

global proj, grp, asst
global elements

__anClass__ = "cel"
__bgClass__ = "bg"
__bgType__ = "background"
__rnClasses__ = ["nr", "mr", "sb", "an"]

class ReadPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        global proj, grp, asst
        global elements

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
        asst = os.getenv("ASST")

        self.projMenu = QtGui.QComboBox()
        self.grpMenu = QtGui.QComboBox()
        self.asstMenu = QtGui.QComboBox()

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

        zero = QtGui.QWidget()
        one = QtGui.QWidget()

        zero.setLayout(QtGui.QHBoxLayout())
        zero.layout().setContentsMargins(2, 2, 2, 2)
        zero.layout().setSpacing(2)
        one.setLayout(QtGui.QHBoxLayout())
        one.layout().setContentsMargins(2, 2, 2, 2)
        one.layout().setSpacing(2)

        zero.layout().addWidget(QtGui.QLabel("project"))
        zero.layout().addWidget(self.projMenu)
        zero.layout().addWidget(QtGui.QLabel("group"))
        zero.layout().addWidget(self.grpMenu)
        zero.layout().addWidget(QtGui.QLabel("asset"))
        zero.layout().addWidget(self.asstMenu)
        zero.layout().addStretch(0)

        tabs = QtGui.QTabWidget()

        elements = ueAssetUtils.getElements(ueSpec.Spec(proj, grp, asst))

        self.animationTab = AnimationTab()
        self.backgroundTab = BackgroundTab()
        self.renderTab = RenderTab()

        tabs.addTab(self.animationTab, "Animation")
        tabs.addTab(self.backgroundTab, "Background")
        tabs.addTab(self.renderTab, "Render")

        one.layout().addWidget(tabs)

        self.layout().addWidget(zero)
        self.layout().addWidget(one)

        self.projMenu.activated.connect(self.loadGroups)
        self.grpMenu.activated.connect(self.loadAssets)
        self.asstMenu.activated.connect(self.loadElements)

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
        global asst, elements
        asst = str(self.asstMenu.currentText())
        elements = ueAssetUtils.getElements(ueSpec.Spec(proj, grp, asst))
        self.animationTab.reload()
        self.backgroundTab.reload()
        self.renderTab.reload()


class AnimationTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.layerListFile = os.getenv("ASST_ROOT")

        self.layerList = QtGui.QListWidget()
        self.passList = QtGui.QListWidget()
        self.versList = QtGui.QListWidget()
        self.layerListPicker = QtGui.QLineEdit()
        self.layerListPickerButton = QtGui.QPushButton("...")
        self.layerButton = QtGui.QPushButton("insert layer")
        self.passButton = QtGui.QPushButton("insert pass")

        zero = QtGui.QWidget()
        one = QtGui.QWidget()
        two = QtGui.QWidget()
        three = QtGui.QWidget()

        zero.setLayout(QtGui.QHBoxLayout())
        zero.layout().setContentsMargins(2, 2, 2, 2)
        zero.layout().setSpacing(2)
        one.setLayout(QtGui.QHBoxLayout())
        one.layout().setContentsMargins(2, 2, 2, 2)
        one.layout().setSpacing(2)
        two.setLayout(QtGui.QHBoxLayout())
        two.layout().setContentsMargins(2, 2, 2, 2)
        two.layout().setSpacing(2)
        three.setLayout(QtGui.QHBoxLayout())
        three.layout().setContentsMargins(2, 2, 2, 2)
        three.layout().setSpacing(2)

        zero.layout().addWidget(QtGui.QLabel("layer"))
        zero.layout().addWidget(QtGui.QLabel("pass"))
        zero.layout().addWidget(QtGui.QLabel("version"))
        one.layout().addWidget(self.layerList)
        one.layout().addWidget(self.passList)
        one.layout().addWidget(self.versList)
        two.layout().addWidget(self.layerListPicker)
        two.layout().addWidget(self.layerListPickerButton)
        three.layout().addWidget(self.layerButton)
        three.layout().addWidget(self.passButton)

        self.layout().addWidget(zero)
        self.layout().addWidget(one)
        self.layout().addWidget(two)
        self.layout().addWidget(three)

        self.reload()

        self.layerList.itemSelectionChanged.connect(self.loadPasses)
        self.passList.itemSelectionChanged.connect(self.loadVersions)
        self.layerListPickerButton.clicked.connect(self.fileBrowser)
        self.layerButton.clicked.connect(self.nukeImportLayer)
        self.passButton.clicked.connect(self.nukeImportPass)

    def fileBrowser(self):
        f = QtGui.QFileDialog.getOpenFileName(self, "Open file",
                                              self.layerListFile,
                                              "Text files (*.txt)")
        if f != None:
            self.layerListFile = f
            self.layerListPicker.setText(self.layerListFile)

    def reload(self):
        self.layerListFile = os.getenv("ASST_ROOT")
        self.layerListPicker.setText(self.layerListFile)
        self.loadLayers()

    def loadLayers(self):
        self.layerList.clear()
        if __anClass__ in elements:
            for l in sorted(elements[__anClass__]):
                self.layerList.addItem(QtGui.QListWidgetItem(l))
            self.layerList.setCurrentItem(self.layerList.item(0))
            self.loadPasses()

    def loadPasses(self):
        self.eltype = str(self.layerList.currentItem().text())
        self.passList.clear()
        if __anClass__ in elements:
            if self.eltype in elements[__anClass__]:
                for c in sorted(elements[__anClass__][self.eltype]):
                    self.passList.addItem(QtGui.QListWidgetItem(c))
                self.passList.setCurrentItem(self.passList.item(0))

                asset = ueAssetUtils.getAsset(ueSpec.Spec(proj, grp, asst))

                f = os.path.join(asset["path"], "tmp", "fromTVP",
                                 self.eltype+"_layerList.txt")

                if os.path.isfile(f):
                    self.layerListFile = f
                    self.layerListPicker.setText(f)
                else:
                    self.layerListFile = os.getenv("ASST_ROOT")
                    self.layerListPicker.setText(self.layerListFile)

                self.loadVersions()

    def loadVersions(self):
        self.elname = str(self.passList.currentItem().text())
        self.versList.clear()
        spec = ueSpec.Spec(proj, grp, asst, __anClass__,
                           self.eltype, self.elname)
        versions = ueAssetUtils.getVersions(spec)
        for v in sorted(range(len(versions)), reverse=True):
            item = QtGui.QListWidgetItem("%04d" % int(v+1))
            self.versList.addItem(item)
        self.versList.setCurrentItem(self.versList.item(0))

    def nukeImportPass(self, name=None, version=None, x=None, y=None):
        if not name:
            name = self.elname

        if not version:
            version = int(self.versList.currentItem().text())

        read = ueNuke.ueReadAsset("Read", name="%s_%s" % (self.eltype, name), inpanel=False)
        reColour = getReColour(["name", "reColour", "postage_stamp", "1"])
        colour = nuke.createNode("Constant", inpanel=False)

        colour.knob("color").setValue(1.0, 0)
        colour.knob("color").setValue(0.0, 1)
        colour.knob("color").setValue(0.0, 2)
        colour.knob("color").setValue(1.0, 3)

        reColour.setInput(0, colour)
        reColour.setInput(1, read)

        if x:
            reColour.setXYpos(x, y)
        else:
            x = reColour.xpos()
            y = reColour.ypos()

        colour.setXYpos(x-100, y)
        read.setXYpos(x, y-140)

        read.knob("proj").setValue(proj)
        read.knob("grp").setValue(grp)
        read.knob("asst").setValue(asst)
        read.knob("elname").setValue(name)
        read.knob("eltype").setValue(self.eltype)
        read.knob("elclass").setValue(__anClass__)
        read.knob("vers").setValue(version)

        return reColour

    def nukeImportLayer(self):
        if self.layerListFile == None:
            return

        f = open(self.layerListFile)
        passes = []
        for elpass in f:
            passes.append(elpass)

        n = []
        x = None
        y = None
        for elpass in reversed(passes):
            elpass = elpass.strip()
            spec = ueSpec.Spec(proj, grp, asst, __anClass__,
                               self.eltype, elpass)
            versions = ueAssetUtils.getVersions(spec)
            node = self.nukeImportPass(name=elpass.strip(), version=len(versions), x=x, y=y)
            x = node.xpos()+200
            y = node.ypos()
            n.append(node)

        f.close()

        for i, nn in enumerate(n):
            if i == 0:
                # Create a dot node
                dot = nuke.nodes.Dot(xpos=nn.xpos(), ypos=nn.ypos())
                dot.setInput(0, nn)
                nn = dot
            if i < len(n)-1:
                # Create the merge
                m = nuke.nodes.Merge(inputs=[nn, n[i+1]])
                n[i+1] = m
            if i == 0:
                y = m.ypos()+20
            m.setXpos(m.xpos())
            m.setYpos(y)

def getReColour(a):
    spec = ueSpec.Spec(proj, "lib", "nuke",
                       "giz", "celUtils", "reColour")
    version = ueAssetUtils.getVersions(spec)[-1]
    return nuke.createNode(version["file_name"], " ".join(a), inpanel=False)


class BackgroundTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.backgroundList = QtGui.QListWidget()
        self.versList = QtGui.QListWidget()
        self.backgroundButton = QtGui.QPushButton("insert background")

        zero = QtGui.QWidget()
        one = QtGui.QWidget()
        two = QtGui.QWidget()

        zero.setLayout(QtGui.QHBoxLayout())
        zero.layout().setContentsMargins(2, 2, 2, 2)
        zero.layout().setSpacing(2)
        one.setLayout(QtGui.QHBoxLayout())
        one.layout().setContentsMargins(2, 2, 2, 2)
        one.layout().setSpacing(2)
        two.setLayout(QtGui.QHBoxLayout())
        two.layout().setContentsMargins(2, 2, 2, 2)
        two.layout().setSpacing(2)

        zero.layout().addWidget(QtGui.QLabel("background"))
        zero.layout().addWidget(QtGui.QLabel("version"))
        one.layout().addWidget(self.backgroundList)
        one.layout().addWidget(self.versList)
        two.layout().addWidget(self.backgroundButton)

        self.layout().addWidget(zero)
        self.layout().addWidget(one)
        self.layout().addWidget(two)

        self.reload()

        self.backgroundList.itemSelectionChanged.connect(self.loadVersions)
        self.backgroundButton.clicked.connect(self.nukeImportBackground)

    def reload(self):
        self.loadBackgrounds()

    def loadBackgrounds(self):
        self.backgroundList.clear()
        if __bgClass__ in elements:
            if __bgType__ in elements[__bgClass__]:
                for b in sorted(elements[__bgClass__][__bgType__]):
                    self.backgroundList.addItem(QtGui.QListWidgetItem(b))
                self.backgroundList.setCurrentItem(self.backgroundList.item(0))

                self.loadVersions()

    def loadVersions(self):
        self.elname = str(self.backgroundList.currentItem().text())
        self.versList.clear()
        spec = ueSpec.Spec(proj, grp, asst, __bgClass__, __bgType__,
                           self.elname)
        vers = ueAssetUtils.getVersions(spec)
        for v in sorted(range(len(vers)), reverse=True):
            item = QtGui.QListWidgetItem("%04d" % int(v+1))
            self.versList.addItem(item)
        self.versList.setCurrentItem(self.versList.item(0))

    def nukeImportBackground(self):
        read = ueNuke.ueReadAsset("Read", name=self.elname, inpanel=False)

        read.knob("proj").setValue(proj)
        read.knob("grp").setValue(grp)
        read.knob("asst").setValue(asst)
        read.knob("elname").setValue(self.elname)
        read.knob("eltype").setValue(__bgType__)
        read.knob("elclass").setValue(__bgClass__)
        read.knob("vers").setValue(int(self.versList.currentItem().text()))


class RenderTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.classList = QtGui.QComboBox()
        self.typeList = QtGui.QListWidget()
        self.nameList = QtGui.QListWidget()
        self.versList = QtGui.QListWidget()
        self.passList = QtGui.QListWidget()
        self.renderButton = QtGui.QPushButton("insert render")

        zero = QtGui.QWidget()
        one = QtGui.QWidget()
        two = QtGui.QWidget()
        three = QtGui.QWidget()
        topWidget = QtGui.QWidget()

        zero.setLayout(QtGui.QHBoxLayout())
        zero.layout().setContentsMargins(2, 2, 2, 2)
        zero.layout().setSpacing(2)
        one.setLayout(QtGui.QHBoxLayout())
        one.layout().setContentsMargins(2, 2, 2, 2)
        one.layout().setSpacing(2)
        two.setLayout(QtGui.QHBoxLayout())
        two.layout().setContentsMargins(2, 2, 2, 2)
        two.layout().setSpacing(2)
        three.setLayout(QtGui.QHBoxLayout())
        three.layout().setContentsMargins(2, 2, 2, 2)
        three.layout().setSpacing(2)

        zero.layout().addWidget(QtGui.QLabel("class"))
        zero.layout().addWidget(self.classList)
        zero.layout().addStretch(0)
        one.layout().addWidget(QtGui.QLabel("type"))
        one.layout().addWidget(QtGui.QLabel("name"))
        one.layout().addWidget(QtGui.QLabel("version"))
        two.layout().addWidget(self.typeList)
        two.layout().addWidget(self.nameList)
        two.layout().addWidget(self.versList)
        three.layout().addWidget(self.renderButton)

        topWidget.setLayout(QtGui.QVBoxLayout())
        topWidget.layout().setContentsMargins(2, 2, 2, 2)
        topWidget.layout().setSpacing(2)
        topWidget.layout().addWidget(zero)
        topWidget.layout().addWidget(one)
        topWidget.layout().addWidget(two)

        self.layout().addWidget(topWidget)
        self.layout().addWidget(QtGui.QLabel("pass"))
        self.layout().addWidget(self.passList)
        self.layout().addWidget(three)

        self.reload()

        self.classList.activated.connect(self.loadTypes)
        self.typeList.itemSelectionChanged.connect(self.loadNames)
        self.nameList.itemSelectionChanged.connect(self.loadVersions)
        self.versList.itemSelectionChanged.connect(self.loadPasses)
        self.renderButton.clicked.connect(self.nukeImportRender)

    def reload(self):
        self.loadClasses()

    def loadClasses(self):
        self.classList.clear()
        for c in sorted(__rnClasses__):
            self.classList.addItem(c)
        self.elclass = str(self.classList.currentText())
        self.loadTypes()

    def loadTypes(self):
        self.elclass = str(self.classList.currentText())
        self.typeList.clear()
        if self.elclass in elements:
            for t in sorted(elements[self.elclass]):
                self.typeList.addItem(QtGui.QListWidgetItem(t))
            self.typeList.setCurrentItem(self.typeList.item(0))
            self.loadNames()

    def loadNames(self):
        self.eltype = str(self.typeList.currentItem().text())
        self.nameList.clear()
        if self.elclass in elements:
            if self.eltype in elements[self.elclass]:
                for n in sorted(elements[self.elclass][self.eltype]):
                    self.nameList.addItem(QtGui.QListWidgetItem(n))
                self.nameList.setCurrentItem(self.nameList.item(0))
                self.loadVersions()

    def loadVersions(self):
        self.elname = str(self.nameList.currentItem().text())
        spec = ueSpec.Spec(proj, grp, asst,
                           self.elclass, self.eltype, self.elname)
        self.versList.clear()
        vers = ueAssetUtils.getVersions(spec)
        if vers:
            for v in sorted(range(len(vers)), reverse=True):
                item = QtGui.QListWidgetItem("%04d" % int(v+1))
                self.versList.addItem(item)
            self.versList.setCurrentItem(self.versList.item(0))
            self.loadPasses()

    def loadPasses(self):
        self.vers = int(self.versList.currentItem().text())

    def nukeImportRender(self):
        read = ueNuke.ueReadAsset("Read", name=self.elname, inpanel=False)

        read.knob("proj").setValue(proj)
        read.knob("grp").setValue(grp)
        read.knob("asst").setValue(asst)
        read.knob("elname").setValue(self.elname)
        read.knob("eltype").setValue(self.eltype)
        read.knob("elclass").setValue(self.elclass)
        read.knob("vers").setValue(int(self.versList.currentItem().text()))

