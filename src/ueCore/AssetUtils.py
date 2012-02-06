import os

import ueClient, ueSpec

import ueCore.Config as ueConfig

def getProject(spec):
    return ueClient.client.getProject(spec)

def getProjectsList():
    projects = []
    for p in ueClient.client.getProjects():
        projects.append(p["name"])
    return projects


def getGroup(spec):
    return ueClient.client.getGroup(spec)

def getGroupsList(spec):
    groups = []
    for g in ueClient.client.getGroups(spec):
        groups.append(g["name"])
    return groups


def getAsset(spec):
    return ueClient.client.getAsset(spec)

def getAssetsList(spec):
    assets = []
    for a in ueClient.client.getAssets(spec):
        assets.append(a["name"])
    return assets


def getElements(spec):
    elements = ueClient.client.getElements(spec)
    elementsDict = {}
    for e in elements:
        if not e["elclass"] in elementsDict:
            elementsDict[e["elclass"]] = {}
        if not e["eltype"] in elementsDict[e["elclass"]]:
            elementsDict[e["elclass"]][e["eltype"]] = {}
        if not e["elname"] in elementsDict[e["elclass"]][e["eltype"]]:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]] = {}
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
    return elementsDict

def getElement(spec):
    e = ueClient.client.getElement(spec)
    elementsDict = {}
    if "elclass" in e and "eltype" in e and "elname" in e:
        if not e["elclass"] in elementsDict:
            elementsDict[e["elclass"]] = {}
        if not e["eltype"] in elementsDict[e["elclass"]]:
            elementsDict[e["elclass"]][e["eltype"]] = {}
        if not e["elname"] in elementsDict[e["elclass"]][e["eltype"]]:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]] = {}
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
    return elementsDict


def getVersions(spec):
    element = ueClient.client.getElement(spec)
    if not "versions" in element:
        element["versions"] = []
    return element["versions"]


def getClasses(spec):
    return {}

def getClass(spec):
    return {}

def getClassesList(spec):
    return []


def getTypesList(spec):
    return []


def getNames(spec):
    return {}

def getNamesList(spec):
    return []


def parsePath(path, **kwargs):
    p = path
    if "vers" in kwargs:
        p = path.replace("%%version%%", "%03d" % kwargs["vers"])
    return p

def getElementPath(spec):
    assetClasses = ueConfig.Config(spec).config.assetClasses

    # Check class
    if spec.elclass not in assetClasses:
        return "Error: Class '%s' not found in asset '%s:%s:%s'" % \
               (spec.elclass, spec.proj, spec.grp, spec.asst)

    # Check type
    # Check name

    element = getAsset(spec)

    prepend = ""
    if "pathprepend" in assetClasses[spec.elclass]:
        prepend = parsePath(assetClasses[spec.elclass]["pathprepend"])

    d = os.path.join(element["path"], prepend, spec.eltype, spec.elname)

    return d

def getVersionPath(spec):
    assetClasses = ueConfig.Config(spec).config.assetClasses

    append = ""
    if "pathappend" in assetClasses[spec.elclass]:
        append = parsePath(assetClasses[spec.elclass]["pathappend"], vers=spec.vers)

    return os.path.join(getElementPath(spec), append)


def getElementName(spec):
    try:
        s = "%s_%s_%s_%s_%s_%s_%04d" % (spec.proj, spec.grp, spec.asst,
                                        spec.elname, spec.eltype,
                                        spec.elclass, spec.vers)
    except TypeError:
        s = "%s_%s_%s_%s_%s_%s_%s" % (spec.proj, spec.grp, spec.asst,
                                      spec.elname, spec.eltype,
                                      spec.elclass, spec.vers)
    return s

