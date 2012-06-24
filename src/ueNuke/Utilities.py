import os

import nuke

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils

def saveUtility(spec, dbMeta={}):
    root = nuke.root()

    e = ueAssetUtils.getElement(spec)
    if e == {}:
        e = ueCreate.createElement(spec, dbMeta=dbMeta)

    v = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = v["version"]

    nkPath = v["path"]
    nkName = v["file_name"]
    f = os.path.join(nkPath, nkName+".nk")

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
        root.addKnob(nuke.Int_Knob("uevers", "vers", spec.vers))
        # Nuke bug? Passing a value into Int_Knob doesn't actually set the value
        # on the knob. Calling setValue explicitly to get around this.
        root.knob("uevers").setValue(spec.vers)
    else:
        root.knob("uevers").setValue(spec.vers)

    if root.knob("version_path") == None:
        root.addKnob(nuke.String_Knob("version_path", "version_path", nkPath))
    else:
        root.knob("version_path").setValue(nkPath)

    nuke.scriptSaveAs(f)

    if "thumbnail" in v:
        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(v["thumbnail"])+".png")
        dest = os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, nkName+".png")
        if not os.path.exists(os.path.dirname(dest)):
            ueFileUtils.createDir(os.path.dirname(dest))
        ueFileUtils.moveFile(source, dest)

    nuke.tprint("Saved %s" % spec)

