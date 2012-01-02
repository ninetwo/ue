import os, sys
import json

import ueCore.ConfigUtils as ueConfigUtils
import ueCore.FileUtils as ueFileUtils
import ueCore.AssetUtils as ueAssetUtils

def parsePath(path, **kwargs):
    p = path
    if "vers" in kwargs:
        p = path.replace("%%version%%", "%03d" % kwargs["vers"])
    return p

def getElementPath(proj, grp, asst, elclass, eltype, name, vers=1):
    config = ueConfigUtils.getConfig(proj, grp, asst)
    assetClasses = config["ASSET_CLASSES"]

    if elclass not in assetClasses:
        return "Error: Class '%s' not found in asset '%s:%s:%s'" % (elclass, proj, grp, asst)

    # Check type
    # Check name

    e = ueAssetUtils.getAsset(proj, grp, asst)

    prepend = ""
    if "pathprepend" in assetClasses[elclass]:
        prepend = parsePath(assetClasses[elclass]["pathprepend"])

#    append = ""
#    if "pathappend" in assetClasses[elclass]:
#        append = parsePath(assetClasses[elclass]["pathappend"], vers=vers)
#
    d = os.path.join(e["path"], prepend, eltype+"-"+elclass, name)

    return d

def getVersionPath(proj, grp, asst, elclass, eltype, name, vers=1):
    config = ueConfigUtils.getConfig(proj, grp, asst)
    assetClasses = config["ASSET_CLASSES"]

    append = ""
    if "pathappend" in assetClasses[elclass]:
        append = parsePath(assetClasses[elclass]["pathappend"], vers=vers)

    return os.path.join(getElementPath(proj, grp, asst, elclass, eltype, name, vers), append)

def getElementName(proj, grp, asst, elclass, eltype, name, vers):
    try:
        s = "%s_%s_%s-%s_%s-%s_%03d" % (proj, grp, asst, name, eltype, elclass, vers)
    except TypeError:
        s = "%s_%s_%s-%s_%s-%s_%s" % (proj, grp, asst, name, eltype, elclass, vers)
    return s

def createElement(proj, grp, asst, elclass, eltype, name):
    asset = ueAssetUtils.getAsset(proj, grp, asst)

    d = getElementPath(proj, grp, asst, elclass, eltype, name)

    ueFileUtils.createDir(d)

    classes = ueAssetUtils.getElements(proj, grp, asst)

    if elclass not in classes:
        classes[elclass] = {}
    if eltype not in classes[elclass]:
        classes[elclass][eltype] = {}

    classes[elclass][eltype][name] = {"path": d}

    p = os.path.join(asset["path"], "etc", "elements")
    try:
        f = open(p, "w")
        f.write(json.dumps(classes, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Adding element to asset element list '%s' (%s)" % (d, e)
        return

    return classes[elclass][eltype][name]

def createVersion(proj, grp, asst, elclass, eltype, name, vers=1, **kwargs):
    element = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    versions = ueAssetUtils.getVersions(proj, grp, asst, elclass, eltype, name)

    verPath = getVersionPath(proj, grp, asst, elclass, eltype, name, vers)

    ueFileUtils.createDir(verPath)

    p = {"path": verPath}
    for k in kwargs:
        p[k] = kwargs[k]

    versions.append(p)

    p = os.path.join(element["path"], "versions")
    try:
        f = open(p, "w")
        f.write(json.dumps(versions, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Adding version to element version list '%s' (%s)" % (element["path"], e)
        return

    return versions[-1]

