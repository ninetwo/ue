import os

import nuke

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate

def saveUtility(spec):
    root = nuke.root()

    if root.knob("proj") == None:
        root.addKnob(nuke.String_Knob("proj", "project", spec.proj))

    if root.knob("grp") == None:
        root.addKnob(nuke.String_Knob("grp", "group", spec.grp))

    if root.knob("asst") == None:
        root.addKnob(nuke.String_Knob("asst", "asset", spec.asst))

    if root.knob("ueclass") == None:
        root.addKnob(nuke.String_Knob("ueclass", "class", spec.elclass))

    if root.knob("uetype") == None:
        root.addKnob(nuke.String_Knob("uetype", "type", spec.eltype))

    if root.knob("uename") == None:
        root.addKnob(nuke.String_Knob("uename", "name", spec.elname))

    if root.knob("asst_root") == None:
        root.addKnob(nuke.String_Knob("asst_root", "asst_root", os.getenv("ASST_ROOT")))

    d = ueAssetUtils.getElement(spec)
    print d
    if d == {}:
        d = ueCreate.createElement(spec)

    p = ueCreate.createVersion(spec)

    spec.vers = p["version"]

    nkName = ueAssetUtils.getElementName(spec)
    nkPath = os.path.join(p["path"], nkName+".nk")

    nuke.scriptSaveAs(nkPath)

    nuke.tprint("Saved %s" % spec)

