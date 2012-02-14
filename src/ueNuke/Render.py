import os

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

    if p.showModalDialog():
        renderOpts = ueCommonRender.getValues()
        nuke.tprint(renderOpts)

    nukescripts.unregisterPanel("ue.panel.ueRender", lambda: "return")

    if renderOpts[0] == 0:
        preRender(n)
        if n.knob("limit_range").value():
            first = n.knob("first").value()
            last = n.knob("last").value()
        else:
            first = nuke.root().knob("first_frame").value()
            last = nuke.root().knob("last_frame").value()
        nuke.execute(n.name()+"."+n.knob("format").value(),
                     int(first), int(last), 1)
        postRender(n)

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

    nuke.toNode(n.name()+"."+n.knob("format").value()).knob("file").setValue(rPath)

    dbMeta = {}
    dbMeta["comment"] = "Auto-save of render %s" % str(destSpec)

    ueNukeUtils.saveUtility(sourceSpec, dbMeta=dbMeta)
    ueNukeUtils.saveUtility(sourceSpec)

    nuke.tprint("Rendering %s to %s ..." % (str(destSpec), os.path.dirname(rPath)))

def postRender(n):
    destSpec = ueSpec.Spec(n.knob("proj").value(),
                           n.knob("grp").value(),
                           n.knob("asst").value(),
                           n.knob("elclass").value(),
                           n.knob("eltype").value(),
                           n.knob("elname").value())

    nuke.tprint("Rendering %s complete" % str(destSpec))

