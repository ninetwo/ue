import os

from PyQt4 import QtCore, QtGui

import maya.cmds
import maya.mel

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate

import ueMaya
import ueMaya.Save as ueSave
import ueMaya.Utilities as ueMayaUtils
import ueCommon.Render as ueCommonRender
import ueCommon.Save as ueCommonSave

def ueRender():
    Render().show()

class Render(QtGui.QMainWindow):
    def __init__(self, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        ueCommonRender.setRenderFrom(getRenderLayerList())
        ueCommonRender.setCurrentRender("defaultRenderLayer")

        self.renderWidget = ueCommonRender.Render()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.renderWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueRender [*]")

        self.buttonBox.accepted.connect(self.render)
        self.buttonBox.rejected.connect(self.close)

    def render(self):
        v = ueCommonRender.getValues()
        SaveRender(v).show()
        self.close()

def getRenderLayerList():
    return maya.cmds.ls(type="renderLayer")

class SaveRender(QtGui.QMainWindow):
    def __init__(self, renderOpts, parent=ueMaya.getMayaWindow()):
        QtGui.QMainWindow.__init__(self, parent)

        self.renderOpts = renderOpts

        ueCommonSave.setClasses(["mr"])

        self.saveWidget = ueCommonSave.Save()
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(QtGui.QVBoxLayout())
        centralWidget.layout().addWidget(self.saveWidget)
        centralWidget.layout().addWidget(self.buttonBox)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("ueSave [*]")

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.close)

    def save(self):
        spec, dbMeta = ueCommonSave.getValues()

        # Check if the scene has been saved       
        if maya.cmds.file(q=True, sn=True) == "":
            ueSave.ueSaveAs()

        sourceSpec = ueSpec.Spec(maya.cmds.fileInfo("ueproj", query=True)[0],
                                 maya.cmds.fileInfo("uegrp", query=True)[0],
                                 maya.cmds.fileInfo("ueasst", query=True)[0],
                                 maya.cmds.fileInfo("ueclass", query=True)[0],
                                 maya.cmds.fileInfo("uetype", query=True)[0],
                                 maya.cmds.fileInfo("uename", query=True)[0],
                                 int(maya.cmds.fileInfo("uevers", query=True)[0]))
        destSpec = spec

        # Create the element(s)/version(s) to render into
        dbMeta = {}
        if len(self.renderOpts[1]) > 1:
            dbMeta["passes"] = ",".join(self.renderOpts[1])
        dbMeta["comment"] = "Render from %s" % str(sourceSpec)

        e = ueAssetUtils.getElement(destSpec)
        if e == {}:
            e = ueCreate.createElement(destSpec, dbMeta=dbMeta)

        # If we're rendering into the last existing version, delete it
        if not renderOpts[2]["newVersion"]:
            versions = ueAssetUtils.getVersions(destSpec)
            destSpec.vers = len(versions)
            ueDestroy.destroyVersion(destSpec)

        if renderOpts[2]["clearLastVersion"]:
            print "deleting files"

        # Create a new version
        v = ueCreate.createVersion(destSpec, dbMeta=dbMeta)

        destSpec.vers = v["version"]

        path = v["path"]
        name = v["file_name"]

        # Set up the render globals
        maya.cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
        maya.cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        if len(self.renderOpts[1]) == 1:
            p = os.path.join(path.replace(os.path.join(os.getenv("ASST_ROOT"), "render")+"/", ""), name)
            maya.cmds.setAttr("defaultRenderGlobals.imageFilePrefix", p, type="string")
        else:
            p = os.path.join(path.replace(os.path.join(os.getenv("ASST_ROOT"), "render")+\
                                          "/", ""), "<RenderPass", name+"_<RenderPass>")
            p = os.path.join("<RenderPass", name+"_<RenderPass>")
            maya.cmds.setAttr("defaultRenderGlobals.imageFilePrefix", p, type="string")

        dbMeta = {}
        dbMeta["comment"] = "Auto-save of render %s" % str(destSpec)

        ueMayaUtils.saveUtility(sourceSpec, dbMeta=dbMeta)
        ueMayaUtils.saveUtility(sourceSpec)

        if self.renderOpts[0] == 0:
            print "Rendering %s ..." % str(destSpec)
            maya.mel.eval("mayaBatchRender")
        elif self.renderOpts[0] == 1:
            print "Spooling %s ..." % str(destSpec)
        elif self.renderOpts[0] == 2:
            print "Spooling to cloud currently not avaliable"

        self.close()

