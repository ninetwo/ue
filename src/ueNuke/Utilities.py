import os

import nuke

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

def saveUtility(proj, grp, asst, elclass, eltype, name):
    root = nuke.root()

    if root.knob("ueclass") == None:
        root.addKnob(nuke.String_Knob("ueclass", "class", elclass))

    if root.knob("uetype") == None:
        root.addKnob(nuke.String_Knob("uetype", "type", eltype))

    if root.knob("uename") == None:
        root.addKnob(nuke.String_Knob("uename", "name", name))

    d = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    if d == None:
        d = ueCreateUtils.createElement(proj, grp, asst, elclass, eltype, name)

    vers = ueAssetUtils.getVersions(proj, grp, asst, elclass, eltype, name)
    nkName = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, len(vers)+1)

    p = ueCreateUtils.createVersion(proj, grp, asst, elclass, eltype, name, len(vers)+1)
    nkPath = os.path.join(p["path"], nkName+".nk")

    nuke.tprint("Saving: '%s'" % nkPath)
    nuke.scriptSaveAs(nkPath)

