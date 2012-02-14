import os

import nuke

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils

def saveUtility(spec, dbMeta={}):
    root = nuke.root()

    d = ueAssetUtils.getElement(spec)
    if d == {}:
        d = ueCreate.createElement(spec, dbMeta=dbMeta)

    p = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = p["version"]

    nkName = ueAssetUtils.getElementName(spec)
    nkPath = os.path.join(p["path"], nkName+".nk")

    if root.knob("ueproj") == None:
        root.addKnob(nuke.String_Knob("ueproj", "project", spec.proj))
    else:
        root.knob("ueproj").setValue(spec.proj)

    if root.knob("uegrp") == None:
        root.addKnob(nuke.String_Knob("uegrp", "group", spec.grp))
    else:
        root.knob("uegrp").setValue(spec.grp)

    if root.knob("ueasst") == None:
        root.addKnob(nuke.String_Knob("ueasst", "asset", spec.asst))
    else:
        root.knob("ueasst").setValue(spec.asst)

    if root.knob("ueclass") == None:
        root.addKnob(nuke.String_Knob("ueclass", "class", spec.elclass))
    else:
        root.knob("ueclass").setValue(spec.elclass)

    if root.knob("uetype") == None:
        root.addKnob(nuke.String_Knob("uetype", "type", spec.eltype))
    else:
        root.knob("uetype").setValue(spec.eltype)

    if root.knob("uename") == None:
        root.addKnob(nuke.String_Knob("uename", "name", spec.elname))
    else:
        root.knob("uename").setValue(spec.elname)

    if root.knob("uevers") == None:
        root.addKnob(nuke.Int_Knob("uevers", "vers", int(p["version"])))
    else:
        root.knob("uevers").setValue(int(p["version"]))

    if root.knob("version_path") == None:
        root.addKnob(nuke.String_Knob("version_path", "version_path", p["path"]))
    else:
        root.knob("version_path").setValue(p["path"])

    nuke.scriptSaveAs(nkPath)

    if "thumbnail" in p:
        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(p["thumbnail"])+".png")
        dest = os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, ueAssetUtils.getElementName(spec)+".png")
        if not os.path.exists(os.path.dirname(dest)):
            ueFileUtils.createDir(os.path.dirname(dest))
        ueFileUtils.moveFile(source, dest)

    nuke.tprint("Saved %s" % spec)

def ueReadNode():
    spec = ueSpec.Spec(os.getenv("PROJ"), "lib", "global",
                       "giz", "fileUtils", "ueRead")
    spec.vers = len(ueAssetUtils.getVersions(spec))
    return ueAssetUtils.getElementName(spec)

def ueWriteNode():
    spec = ueSpec.Spec(os.getenv("PROJ"), "lib", "global",
                       "giz", "fileUtils", "ueWrite")
    spec.vers = len(ueAssetUtils.getVersions(spec))
    return ueAssetUtils.getElementName(spec)

