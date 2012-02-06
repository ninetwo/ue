import sys, os

from PyQt4 import QtCore, QtGui

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

global proj, grp, asst

class ReadPanel(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        global proj, grp, asst

        proj = os.getenv("PROJ")
        grp = os.getenv("GRP")
        asst = os.getenv("ASST")

        self.projMenu = QtGui.QComboBox()
        self.grpMenu = QtGui.QComboBox()
        self.asstMenu = QtGui.QComboBox()

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
        global asst
        asst = str(self.asstMenu.currentText())
        self.animationTab.reload()
        self.backgroundTab.reload()
        self.renderTab.reload()

class AnimationTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.elclass = "cel"
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

        zero.layout().addWidget(QtGui.QLabel("layers"))
        zero.layout().addWidget(QtGui.QLabel("passes"))
        zero.layout().addWidget(QtGui.QLabel("versions"))
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

        self.connect(self.layerList,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.loadPasses)
        self.connect(self.passList,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.loadVersions)
        self.connect(self.layerListPickerButton,
                     QtCore.SIGNAL("clicked()"),
                     self.fileBrowser)
        self.connect(self.layerButton,
                     QtCore.SIGNAL("clicked()"),
                     self.nukeImportLayer)
        self.connect(self.passButton,
                     QtCore.SIGNAL("clicked()"),
                     self.nukeImportPass)

    def fileBrowser(self):
        f = QtGui.QFileDialog.getOpenFileName(self, "Open file",
                                              self.layerListFile,
                                              "Text files (*.txt)")
        if not f == None:
            self.layerList = f
            self.layerListPicker.setText(f)

    def reload(self):
        spec = ueSpec.Spec(proj, grp, asst, self.elclass)
        self.layers = ueAssetUtils.getClass(spec)

        if self.layers == None:
            self.layers = {}

        self.layerListFile = os.getenv("ASST_ROOT")
        self.layerListPicker.setText(os.getenv("ASST_ROOT"))

        self.loadLayers()

    def loadLayers(self):
        self.layerList.clear()
        for l in self.layers:
            self.layerList.addItem(QtGui.QListWidgetItem(l))
        self.passList.clear()

    def loadPasses(self):
        self.passList.clear()
        if str(self.layerList.currentItem().text()) in self.layers:
            for c in self.layers[str(self.layerList.currentItem().text())]:
                self.passList.addItem(QtGui.QListWidgetItem(c))
                elpass = c

            f = os.path.join(os.path.dirname(self.layers[str(self.layerList.currentItem().text())][elpass]["path"]),
                         str(self.layerList.currentItem().text())+"_layerList.txt")

            if os.path.isfile(f):
                self.layerListFile = f
                self.layerListPicker.setText(f)
            else:
                self.layerListFile = os.getenv("ASST_ROOT")
                self.layerListPicker.setText(os.getenv("ASST_ROOT"))

    def loadVersions(self):
        self.versList.clear()
        spec = ueSpec.Spec(proj, grp, asst, self.elclass,
                                        str(self.layerList.currentItem().text()),
                                        str(self.passList.currentItem().text()))
        vers = ueAssetUtils.getVersions(spec)
        for v in sorted(range(len(vers)), reverse=True):
            item = QtGui.QListWidgetItem("%3d" % int(v+1))
            self.versList.addItem(item)
            if v+1 == len(vers):
                self.versList.setCurrentItem(item)

    def nukeImportPass(self):
        args = ["proj", proj, "grp", grp, "asst", asst, "elclass", self.elclass,
                "eltype", str(self.layerList.currentItem().text()),
                "elname", str(self.passList.currentItem().text()),
                "vers", str(self.versList.currentItem().text()),
                "postage_stamp", "0",
                "name", "ueRead"]
        read = getUeRead(args)
        #tvpReformat = getTvpReformat(["name", "tvpReformat"])
        reColour = getReColour(["name", "reColour", "postage_stamp", "1"])
        colour = nuke.createNode("Constant", inpanel=False)

        reColour.setInput(0, colour)
        reColour.setInput(1, read)#tvpReformat)

        x = reColour.xpos()
        y = reColour.ypos()

        colour.setXYpos(x-100, y)
        #tvpReformat.setXYpos(x, y-30)
        read.setXYpos(x, y-80)

    def nukeImportLayer(self):
        n = []
        for c in config["tvp"][str(self.layerList.currentItem().text())]:
            n.append(nuke.nodes.Read(name=str(self.layerList.currentItem().text())+"_"+c,
                                     file=config["tvp"][str(self.layerList.currentItem().text())][c]["path"]))
        for nn in n:
            if nn == 0:
                print "Yes"
            m = nuke.nodes.Merge(inputs=[nn, n[n.index(nn)+1]])
            n[n.index(nn)+1] = m

def getUeRead(a):
    spec = ueSpec.Spec(proj, "lib", "global",
                       "giz", "fileUtils", "ueRead")
    v = ueAssetUtils.getVersions(spec)
    spec.vers = len(v)
    n = ueAssetUtils.getElementName(spec)
    return nuke.createNode(n, " ".join(a), inpanel=False)

def getTvpReformat(a):
    spec = ueSpec.Spec(proj, "lib", "global",
                       "giz", "fileUtils", "tvpReformat")
    v = ueAssetUtils.getVersions(spec)
    spec.vers = len(v)
    n = ueAssetUtils.getElementName(spec)
    return nuke.createNode(n, " ".join(a), inpanel=False)

def getReColour(a):
    spec = ueSpec.Spec(proj, "lib", "global",
                       "giz", "celUtils", "reColour")
    v = ueAssetUtils.getVersions(spec)
    spec.vers = len(v)
    n = ueAssetUtils.getElementName(spec)
    return nuke.createNode(n, " ".join(a), inpanel=False)


class BackgroundTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.elclass = "bg"
        self.eltype = "background"

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

        zero.layout().addWidget(QtGui.QLabel("backgrounds"))
        one.layout().addWidget(self.backgroundList)
        one.layout().addWidget(self.versList)
        two.layout().addWidget(self.backgroundButton)

        self.layout().addWidget(zero)
        self.layout().addWidget(one)
        self.layout().addWidget(two)

        self.reload()

        self.connect(self.backgroundList,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.loadVersions)
        self.connect(self.backgroundButton,
                     QtCore.SIGNAL("clicked()"),
                     self.nukeImportBackground)

    def reload(self):
        spec = ueSpec.Spec(proj, grp, asst, self.elclass, self.eltype)
        self.backgrounds = ueAssetUtils.getNamesList(spec)

        self.loadBackgrounds()

    def loadBackgrounds(self):
        self.backgroundList.clear()
        for b in self.backgrounds:
            self.backgroundList.addItem(QtGui.QListWidgetItem(b))

    def loadVersions(self):
        self.versList.clear()
        spec = ueSpec.Spec(proj, grp, asst, self.elclass, self.eltype,
                           str(self.backgroundList.currentItem().text()))
        vers = ueAssetUtils.getVersions(spec)
        for v in sorted(range(len(vers)), reverse=True):
            item = QtGui.QListWidgetItem("%3d" % int(v+1))
            self.versList.addItem(item)
            if v+1 == len(vers):
                self.versList.setCurrentItem(item)

    def nukeImportBackground(self):
        print "test"


class RenderTab(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self.elclass = ["cp", "rn"]

        self.classList = QtGui.QComboBox()
        self.typeList = QtGui.QListWidget()
        self.nameList = QtGui.QListWidget()
        self.versList = QtGui.QListWidget()
        self.renderButton = QtGui.QPushButton("insert render")

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

        self.layout().addWidget(zero)
        self.layout().addWidget(one)
        self.layout().addWidget(two)
        self.layout().addWidget(three)

        self.reload()

        self.classList.activated.connect(self.loadTypes)
        self.connect(self.typeList,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.loadNames)
        self.connect(self.nameList,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.loadVersions)
        self.connect(self.renderButton,
                     QtCore.SIGNAL("clicked()"),
                     self.nukeImportRender)

    def reload(self):
        self.loadClasses()

    def loadClasses(self):
        self.classList.clear()
        for c in self.elclass:
            self.classList.addItem(c)
        self.loadTypes()

    def loadTypes(self):
        spec = ueSpec.Spec(proj, grp, asst, str(self.classList.currentText()))
        self.renders = ueAssetUtils.getClass(spec)

        if self.renders == None:
            self.renders = {}

        self.typeList.clear()
        for t in self.renders:
            self.typeList.addItem(QtGui.QListWidgetItem(t))
        

    def loadNames(self):
        self.nameList.clear()
        if str(self.typeList.currentItem().text()) in self.renders:
            for n in self.renders[str(self.typeList.currentItem().text())]:
                self.nameList.addItem(QtGui.QListWidgetItem(n))

    def loadVersions(self):
        spec = ueSpec.Spec(proj, grp, asst,
                                        str(self.classList.currentText()),
                                        str(self.typeList.currentItem().text()),
                                        str(self.nameList.currentItem().text()))
        self.versList.clear()
        vers = ueAssetUtils.getVersions(spec)
        for v in sorted(range(len(vers)), reverse=True):
            item = QtGui.QListWidgetItem("%3d" % int(v+1))
            self.versList.addItem(item)
            if v+1 == len(vers):
                self.versList.setCurrentItem(item)

    def nukeImportRender(self):
        nuke.tprint("import render")
