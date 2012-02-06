import os

import maya.cmds

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueMaya

def saveUtility(spec):
    fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

    if not "ueproj" in fi:
        maya.cmds.fileInfo("ueproj", spec.proj)

    if not "uegrp" in fi:
        maya.cmds.fileInfo("uegrp", spec.grp)

    if not "ueasst" in fi:
        maya.cmds.fileInfo("ueasst", spec.asst)

    if not "ueclass" in fi:
        maya.cmds.fileInfo("ueclass", spec.elclass)

    if not "uetype" in fi:
        maya.cmds.fileInfo("uetype", spec.eltype)

    if not "uename" in fi:
        maya.cmds.fileInfo("uename", spec.elname)

    if not "asst_root" in fi:
        maya.cmds.fileInfo("asst_root", os.getenv("ASST_ROOT"))

    d = ueAssetUtils.getElement(spec)
    if d == {}:
        d = ueCreate.createElement(spec)

    p = ueCreate.createVersion(spec)

    spec.vers = p["version"]

    maName = ueAssetUtils.getElementName(spec)
    maPath = os.path.join(p["path"], maName+".ma")

    maya.cmds.file(rename=maPath)
    maya.cmds.file(save=True, type="mayaAscii")

    print "Saved %s" % spec

