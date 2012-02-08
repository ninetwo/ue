import os

import maya.cmds
import maya.mel

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueMaya

def saveUtility(spec, dbMeta={}, fileType="ma", export=False):
    fileTypes = {"ma": ("mayaAscii", ""),
                 "obj": ("OBJexport", "groups=0; ptgroups=0; materials=0; smoothing=0; normals=0"),
                 "fbx": ()}

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
        d = ueCreate.createElement(spec, dbMeta=dbMeta)

    p = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = p["version"]

    maName = ueAssetUtils.getElementName(spec)
    maPath = os.path.join(p["path"], maName+"."+fileType)

    if fileType == "obj":
        maya.cmds.loadPlugin("objExport.so")
    elif fileType == "fbx":
        maya.cmds.loadPlugin("fbxmaya.so")

    if export:
        if fileType == "fbx":
            maya.mel.eval("FBXExport -f \""+maPath+"\";")
        else:
            maya.cmds.file(maPath, exportSelected=True,
                           options=fileTypes[fileType][1],
                           type=fileTypes[fileType][0])
    else:
        maya.cmds.file(rename=maPath)
        maya.cmds.file(save=True,
                       type=fileTypes[fileType][0])

#    if "thumbnail" in p:
#        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(p["thumbnail"])+".png")
#        dest = ueAssetUtils.getThumbnailPath(spec)
#        if not os.path.exists(os.path.dirname(dest)):
#            ueFileUtils.createDir(os.path.dirname(dest))
#        ueFileUtils.moveFile(source, dest)

    print "Saved %s" % spec

