import os

import nuke

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils

def saveUtility(spec, dbMeta={}):
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
    if d == {}:
        d = ueCreate.createElement(spec, dbMeta=dbMeta)

    p = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = p["version"]

    nkName = ueAssetUtils.getElementName(spec)
    nkPath = os.path.join(p["path"], nkName+".nk")

    nuke.scriptSaveAs(nkPath)

    if "thumbnail" in p:
        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(p["thumbnail"])+".png")
        dest = os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, ueAssetUtils.getElementName(spec)+".png")
        if not os.path.exists(os.path.dirname(dest)):
            ueFileUtils.createDir(os.path.dirname(dest))
        ueFileUtils.moveFile(source, dest)

    nuke.tprint("Saved %s" % spec)

