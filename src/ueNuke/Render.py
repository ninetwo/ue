import os, json

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueNuke.Save as ueNukeSave
import ueNuke.Utilities as ueNukeUtils
import ueCommon.Render as ueCommonRender

def ueRender(n):
    p = nukescripts.registerWidgetAsPanel("ueCommonRender.Render", "ueRender",
                                          "ue.panel.ueRender", create=True)
    ueCommonRender.setRenderFrom(getWriteNodeList())

    if p.showModalDialog():
        renderOpts = ueCommonRender.getValues()

        # Make sure the element we're rendering to exists and that the script
        # has been saved
        sourceSpec, destSpec = preRender(n)

        # Get the frame range from the ueWrite gizmo, else default to
        # the scripts asset settings
        if n.knob("limit_range").value():
            first = n.knob("first").value()
            last = n.knob("last").value()
        else:
            first = nuke.root().knob("first_frame").value()
            last = nuke.root().knob("last_frame").value()

        # Render
        # 0 = Standard nuke "interactive" render
        # 1 = DrQueue render farm (os.system is a little weird, but it's
        #     so you don't have to compile it's python module for nuke)
        # 2 = Cloud render farm, maybe sometime in the future
        if renderOpts[0] == 0:
            nuke.tprint("Rendering %s ..." % str(destSpec))
            nuke.execute(n.name()+"."+n.knob("format").value(),
                         int(first), int(last), 1)
        elif renderOpts[0] == 1:
            nuke.tprint("Spooling %s ..." % str(destSpec))
            sourceSpec.vers = sourceSpec.vers-1
            options = {}
            options["writeNode"] = n.name()+"."+n.knob("format").value()
            p = os.path.join(os.getenv("UE_PATH"), "src", "ueRender", "Spool.py")
            os.system("python %s %s %s nuke %i %i '%s'" % (p, str(sourceSpec), str(destSpec),
                                                           int(first), int(last),
                                                           json.dumps(options)))
        elif renderOpts[0] == 2:
            nuke.tprint("Spooling to cloud currently not avaliable")

    nukescripts.unregisterPanel("ue.panel.ueRender", lambda: "return")

def preRender(n):
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

    destSpec = ueSpec.Spec(n.knob("proj").value(),
                           n.knob("grp").value(),
                           n.knob("asst").value(),
                           n.knob("elclass").value(),
                           n.knob("eltype").value(),
                           n.knob("elname").value())

    dbMeta = {}
    dbMeta["comment"] = "Render from %s" % str(sourceSpec)

    d = ueAssetUtils.getElement(destSpec)
    if d == {}:
        d = ueCreate.createElement(destSpec, dbMeta=dbMeta)

    p = ueCreate.createVersion(destSpec, dbMeta=dbMeta)

    destSpec.vers = p["version"]

    rName = ueAssetUtils.getElementName(destSpec)
    rPath = os.path.join(p["path"], rName+".%04d.exr")

    n.knob("file").setValue(rPath)

    dbMeta = {}
    dbMeta["comment"] = "Auto-save of render %s" % str(destSpec)

    ueNukeUtils.saveUtility(sourceSpec, dbMeta=dbMeta)
    ueNukeUtils.saveUtility(sourceSpec)

    return sourceSpec, destSpec

def postRender(n):
    destSpec = ueSpec.Spec(n.knob("proj").value(),
                           n.knob("grp").value(),
                           n.knob("asst").value(),
                           n.knob("elclass").value(),
                           n.knob("eltype").value(),
                           n.knob("elname").value())

    nuke.tprint("Rendering %s complete" % str(destSpec))

def getWriteNodeList():
    nodes = nuke.allNodes(ueNukeUtils.ueWriteNode(), nuke.root())
    nodeList = []
    for n in nodes:
        nodeList.append(n.name())
    return nodeList

