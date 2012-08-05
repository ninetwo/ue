import os, json

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils
import ueCore.Destroy as ueDestroy

import ueNuke.Save as ueNukeSave
import ueNuke.Utilities as ueNukeUtils

import ueCommon.Render as ueCommonRender
import ueCommon.Save as ueCommonSave

def ueRender(foo, currentNode=None):
    p = nukescripts.registerWidgetAsPanel("ueCommonRender.Render", "ueRender",
                                          "ue.panel.ueRender", create=True)
    ueCommonRender.setRenderFrom(getWriteNodeList())
    ueCommonRender.setCurrentRender(currentNode)

    if p.showModalDialog():
        runRender(ueCommonRender.getValues())

    nukescripts.unregisterPanel("ue.panel.ueRender", lambda: "return")

def runRender(renderOpts):
    root = nuke.root()

    if root.name() == "Root":
        ueNukeSave.ueSaveAs()

    sourceSpec = ueSpec.Spec(root.knob("ueproj").value(),
                             root.knob("uegrp").value(),
                             root.knob("ueasst").value(),
                             root.knob("ueclass").value(),
                             root.knob("uetype").value(),
                             root.knob("uename").value(),
                             root.knob("uevers").value())

    writeNodes = []
    frameRanges = []
    for i, writeNode in enumerate(renderOpts[1]):
        n = nuke.toNode(writeNode)

        destSpec = ueSpec.Spec(n.knob("proj").value(),
                               n.knob("grp").value(),
                               n.knob("asst").value(),
                               n.knob("elclass").value(),
                               n.knob("eltype").value(),
                               n.knob("elname").value())

        # Create the element(s)/version(s) to render into
        dbMeta = {}

        e = ueAssetUtils.getElement(destSpec)
        if e == {}:
            e = ueCreate.createElement(destSpec, dbMeta=dbMeta)

        # If we're rendering into the last existing version, delete it
        if not renderOpts[2]["newVersion"]:
            versions = ueAssetUtils.getVersions(destSpec)
            destSpec.vers = len(versions)
            ueDestroy.destroyVersion(destSpec)

        if renderOpts[2]["clearLastVersion"]:
            nuke.tprint("deleting files")

        # Create a new version
        dbMeta["comment"] = "Render from %s" % str(sourceSpec)
        v = ueCreate.createVersion(destSpec, dbMeta=dbMeta)

        destSpec.vers = v["version"]

        path = v["path"]
        name = v["file_name"]

        # Set up the write nodes with the correct paths
        p = os.path.join(path, name+".%04d."+n.knob("file_type").value())
        n.knob("file").setValue(p)

        # Get the frame range from the ueWrite gizmo, else default to
        # the scripts asset settings
        first = nuke.root().knob("first_frame").value()
        last = nuke.root().knob("last_frame").value()
        if n.knob("use_limit").value():
            first = n.knob("first").value()
            last = n.knob("last").value()

        writeNodes.append(n)
        if i == 0:
            frameRanges.append((int(first), int(last), 1))
        else:
            frameRanges.append((int(first), int(first), 1))

    dbMeta = {}
    dbMeta["comment"] = "Auto-save of render %s" % str(destSpec)

    ueNukeUtils.saveUtility(sourceSpec, dbMeta=dbMeta)
    ueNukeUtils.saveUtility(sourceSpec)

    # Render
    # 0 = Standard nuke "interactive" render
    # 1 = DrQueue render farm (os.system is a little weird, but it's
    #     so you don't have to compile it's python module for nuke)
    # 2 = Cloud render farm, maybe sometime in the future
    if renderOpts[0] == 0:
        nuke.tprint("Rendering %s ..." % str(destSpec))
        # execute() takes a string for the node name, executeMultiple() takes a tuple of node objects
        if len(writeNodes) == 1:
            nuke.execute(writeNodes[0].name(), frameRanges[0][0], frameRanges[0][1], frameRanges[0][2])
        else:
            nuke.executeMultiple(tuple(writeNodes), tuple(frameRanges))
    elif renderOpts[0] == 1:
        nuke.tprint("Spooling %s ..." % str(destSpec))
        sourceSpec.vers = sourceSpec.vers-1
        options = {}
        options["writeNode"] = []
        for render in renderOpts[1]:
            n = nuke.toNode(render)
            options["writeNode"].append(n.name())
        p = os.path.join(os.getenv("UE_PATH"), "src", "ueRender", "Spool.py")
        os.system("python %s %s %s nuke %i %i '%s'" % (p, str(sourceSpec), str(destSpec),
                                                       int(first), int(last),
                                                       json.dumps(options)))
    elif renderOpts[0] == 2:
        nuke.tprint("Spooling to cloud currently not avaliable")

def getWriteNodeList():
    nodes = nuke.allNodes("Write", nuke.root())
    nodeList = []
    for n in nodes:
        nodeList.append(n.name())
    return nodeList

