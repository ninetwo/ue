import os

import pymel.core.system
#import maya.cmds

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

def saveUtility(proj, grp, asst, elclass, eltype, name):
    d = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    if d == None:
        d = ueCreateUtils.createElement(proj, grp, asst, elclass, eltype, name)

    vers = ueAssetUtils.getVersions(proj, grp, asst, elclass, eltype, name)
    maName = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, len(vers)+1)

    p = ueCreateUtils.createVersion(proj, grp, asst, elclass, eltype, name, len(vers)+1)
    maPath = os.path.join(p["path"], maName+".ma")

#    nuke.tprint("Saving: '%s'" % maPath)
    pymel.core.system.saveAs(maPath)
#    maya.cmds.file(rename=maPath)
#    maya.cmds.file(save=True, type="mayaAscii")

