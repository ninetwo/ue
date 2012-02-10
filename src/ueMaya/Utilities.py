import os

import maya.cmds
import maya.mel

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueMaya

__fileTypes__ = {"ma": ("mayaAscii", ""),
                 "obj": ("OBJexport", "groups=0; ptgroups=0; materials=0; smoothing=0; normals=0"),
                 "fbx": ()}

def saveUtility(spec, dbMeta={}, fileType="ma", export=False):
    fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

    d = ueAssetUtils.getElement(spec)
    if d == {}:
        d = ueCreate.createElement(spec, dbMeta=dbMeta)

    p = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = p["version"]

    maName = ueAssetUtils.getElementName(spec)
    maPath = os.path.join(p["path"], maName+"."+fileType)

    maya.cmds.fileInfo("ueproj", spec.proj)
    maya.cmds.fileInfo("uegrp", spec.grp)
    maya.cmds.fileInfo("ueasst", spec.asst)
    maya.cmds.fileInfo("ueclass", spec.elclass)
    maya.cmds.fileInfo("uetype", spec.eltype)
    maya.cmds.fileInfo("uename", spec.elname)
    maya.cmds.fileInfo("uevers", spec.vers)
    maya.cmds.fileInfo("version_path", p["path"])

    if fileType == "obj":
        maya.cmds.loadPlugin("objExport.so")
    elif fileType == "fbx":
        maya.cmds.loadPlugin("fbxmaya.so")

    if export:
        if fileType == "fbx":
            maya.mel.eval("FBXExport -f \""+maPath+"\";")
        else:
            maya.cmds.file(maPath, exportSelected=True,
                           options=__fileTypes__[fileType][1],
                           type=__fileTypes__[fileType][0])
    else:
        maya.cmds.file(rename=maPath)
        maya.cmds.file(save=True,
                       type=__fileTypes__[fileType][0])

#    if "thumbnail" in p:
#        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(p["thumbnail"])+".png")
#        dest = ueAssetUtils.getThumbnailPath(spec)
#        if not os.path.exists(os.path.dirname(dest)):
#            ueFileUtils.createDir(os.path.dirname(dest))
#        ueFileUtils.moveFile(source, dest)

    print "Saved %s" % spec

