import os

import maya.cmds
import maya.mel

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueMaya

__fileTypes__ = {
                 "ma":  ("mayaAscii", ""),
                 "obj": ("OBJexport", "groups=0; ptgroups=0; materials=0; smoothing=0; normals=0"),
                 "fbx": ()
                }

def saveUtility(spec, dbMeta={}, fileType="ma", export=False, animated=False):
    fi = ueMaya.parseFileInfo(maya.cmds.fileInfo(query=True))

    e = ueAssetUtils.getElement(spec)
    if e == {}:
        e = ueCreate.createElement(spec, dbMeta=dbMeta)

    v = ueCreate.createVersion(spec, dbMeta=dbMeta)

    spec.vers = v["version"]

    maPath = v["path"]
    maName = v["file_name"]

    f = os.path.join(maPath, maName+"."+fileType)

    # Load plugins needed for export
    if fileType == "obj":
        maya.cmds.loadPlugin("objExport.so")
    elif fileType == "fbx":
        maya.cmds.loadPlugin("fbxmaya.so")

    # Export or save
    if export:
        if fileType == "fbx":
            maya.mel.eval("FBXExport -f \""+f+"\";")
        else:
            if animated:
                start = int(maya.cmds.playbackOptions(query=True, minTime=True))
                end = int(maya.cmds.playbackOptions(query=True, maxTime=True))
                for i in range(start, end):
                    maya.cmds.currentTime(i, edit=True)
                    f = os.path.join(maPath, "%s.%04d.%s" % (maName, i, fileType))
                    maya.cmds.file(f, exportSelected=True,
                                   options=__fileTypes__[fileType][1],
                                   type=__fileTypes__[fileType][0])
            else:
                maya.cmds.file(f, exportSelected=True,
                               options=__fileTypes__[fileType][1],
                               type=__fileTypes__[fileType][0])
    else:
        maya.cmds.fileInfo("ueproj", spec.proj)
        maya.cmds.fileInfo("uegrp", spec.grp)
        maya.cmds.fileInfo("ueasst", spec.asst)
        maya.cmds.fileInfo("ueclass", spec.elclass)
        maya.cmds.fileInfo("uetype", spec.eltype)
        maya.cmds.fileInfo("uename", spec.elname)
        maya.cmds.fileInfo("uevers", spec.vers)
        maya.cmds.fileInfo("version_path", maPath)

        maya.cmds.file(rename=f)
        maya.cmds.file(save=True,
                       type=__fileTypes__[fileType][0])

#    if "thumbnail" in p:
#        source = os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_"+str(p["thumbnail"])+".png")
#        dest = ueAssetUtils.getThumbnailPath(spec)
#        if not os.path.exists(os.path.dirname(dest)):
#            ueFileUtils.createDir(os.path.dirname(dest))
#        ueFileUtils.moveFile(source, dest)

    print "Saved %s" % spec

