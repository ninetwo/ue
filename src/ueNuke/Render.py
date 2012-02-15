import os, json

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils
import ueNuke.Save as ueNukeSave
import ueNuke.Utilities as ueNukeUtils
import ueCommon.Render as ueCommonRender
import ueCommon.Save as ueCommonSave

def ueRender():
    p = nukescripts.registerWidgetAsPanel("ueCommonRender.Render", "ueRender",
                                          "ue.panel.ueRender", create=True)
    ueCommonRender.setRenderFrom(getWriteNodeList())

    if p.showModalDialog():
        root = nuke.root()
        renderOpts = ueCommonRender.getValues()

        if root.name() == "Root":
            ueNukeSave.ueSaveAs()

        sourceSpec = ueSpec.Spec(root.knob("ueproj").value(),
                                 root.knob("uegrp").value(),
                                 root.knob("ueasst").value(),
                                 root.knob("ueclass").value(),
                                 root.knob("uetype").value(),
                                 root.knob("uename").value(),
                                 root.knob("uevers").value())
        destSpec = None

        if len(renderOpts[1]) == 1:
            n = nuke.toNode(renderOpts[1][0])
            destSpec = ueSpec.Spec(n.knob("proj").value(),
                                   n.knob("grp").value(),
                                   n.knob("asst").value(),
                                   n.knob("elclass").value(),
                                   n.knob("eltype").value(),
                                   n.knob("elname").value())
        elif len(renderOpts[1]) > 1:
            p = nukescripts.registerWidgetAsPanel("ueCommonSave.Save", "ueSave",
                                                  "ue.panel.ueSave", create=True)

            p.setMinimumSize(400, 600)
            ueCommonSave.setClasses(["nr"])

            if p.showModalDialog():
                destSpec, dbMeta = ueCommonSave.getValues()

            nukescripts.unregisterPanel("ue.panel.ueSave", lambda: "return")
        else:
            return

        if destSpec == None:
            return

        dbMeta = {}
        dbMeta["passes"] = ",".join(renderOpts[1])

        # Create the element(s)/version(s) to render into
        path, name = createElement(sourceSpec, destSpec, dbMeta)

        # Set up the write nodes with the correct paths
        if len(renderOpts[1]) == 1:
            n = nuke.toNode(renderOpts[1][0])
            p = os.path.join(path, name+".%04d.exr")
            n.knob("file").setValue(p)
        else:
            for render in renderOpts[1]:
                n = nuke.toNode(render)
                p = os.path.join(path, render, name+"_"+render+".%04d.exr")
                if not os.path.exists(os.path.dirname(p)):
                    ueFileUtils.createDir(os.path.dirname(p))
                n.knob("file").setValue(p)

        # Get the frame range from the ueWrite gizmo, else default to
        # the scripts asset settings
        first = nuke.root().knob("first_frame").value()
        last = nuke.root().knob("last_frame").value()
        if len(renderOpts[1]) == 1:
            n = nuke.toNode(renderOpts[1][0])
            if n.knob("limit_range").value():
                first = n.knob("first").value()
                last = n.knob("last").value()

        # Render
        # 0 = Standard nuke "interactive" render
        # 1 = DrQueue render farm (os.system is a little weird, but it's
        #     so you don't have to compile it's python module for nuke)
        # 2 = Cloud render farm, maybe sometime in the future
        if renderOpts[0] == 0:
            nuke.tprint("Rendering %s ..." % str(destSpec))
            if len(renderOpts[1]) == 1:
                nuke.execute(n.name()+"."+n.knob("format").value(),
                             int(first), int(last), 1)
            else:
                writeNodes = []
                frameRanges = []
                for render in renderOpts[1]:
                    n = nuke.toNode(render)
                    writeNodes.append(nuke.toNode(n.name()+"."+n.knob("format").value()))
                    frameRanges.append(tuple([int(first), int(last), 1]))
                nuke.executeMultiple(tuple(writeNodes), tuple(frameRanges))
        elif renderOpts[0] == 1:
            nuke.tprint("Spooling %s ..." % str(destSpec))
            sourceSpec.vers = sourceSpec.vers-1
            options = {}
            options["writeNode"] = []
            for render in renderOpts[1]:
                n = nuke.toNode(render)
                options["writeNode"].append(n.name()+"."+n.knob("format").value())
            p = os.path.join(os.getenv("UE_PATH"), "src", "ueRender", "Spool.py")
            os.system("python %s %s %s nuke %i %i '%s'" % (p, str(sourceSpec), str(destSpec),
                                                           int(first), int(last),
                                                           json.dumps(options)))
        elif renderOpts[0] == 2:
            nuke.tprint("Spooling to cloud currently not avaliable")

    nukescripts.unregisterPanel("ue.panel.ueRender", lambda: "return")

def createElement(sourceSpec, destSpec, dbMeta):
    dbMeta["comment"] = "Render from %s" % str(sourceSpec)

    e = ueAssetUtils.getElement(destSpec)
    if e == {}:
        e = ueCreate.createElement(destSpec, dbMeta=dbMeta)

    v = ueCreate.createVersion(destSpec, dbMeta=dbMeta)

    destSpec.vers = v["version"]

    name = ueAssetUtils.getElementName(destSpec)

    dbMeta = {}
    dbMeta["comment"] = "Auto-save of render %s" % str(destSpec)

    ueNukeUtils.saveUtility(sourceSpec, dbMeta=dbMeta)
    ueNukeUtils.saveUtility(sourceSpec)

    return v["path"], name

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

