"""Returns information on ue assets and elements

Read-only functions for returning information on ue
assets and elements.
"""

import os

import ueClient, ueSpec

def getProject(spec):
    return ueClient.client.getProject(spec)

def getProjects():
    return ueClient.client.getProjects()

def getProjectsList():
    projects = []
    for p in ueClient.client.getProjects():
        projects.append(p["name"])
    return projects


def getGroup(spec):
    return ueClient.client.getGroup(spec)

def getGroups(spec):
    return ueClient.client.getGroups(spec)

def getGroupsList(spec):
    groups = []
    for g in ueClient.client.getGroups(spec):
        groups.append(g["name"])
    return groups


def getAsset(spec):
    return ueClient.client.getAsset(spec)

def getAssets(spec):
    return ueClient.client.getAssets(spec)

def getAssetsList(spec):
    assets = []
    for a in ueClient.client.getAssets(spec):
        assets.append(a["name"])
    return assets


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
        if "comment" in e:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["comment"] = e["comment"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
    return elementsDict

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
        if "comment" in e:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["comment"] = e["comment"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
    return elementsDict


def getVersions(spec):
    element = ueClient.client.getElement(spec)
    if not "versions" in element:
        element["versions"] = []
    return element["versions"]


def parsePath(path, **kwargs):
    p = path
    if "vers" in kwargs:
        p = path.replace("%%version%%", "%04d" % int(kwargs["vers"]))
    return p

def getElementPath(spec, assetClasses=None):
    if assetClasses == None:
        assetClasses = ueConfig.Config(spec).config["assetClasses"]

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

def getVersionPath(spec, assetClasses=None):
    if assetClasses == None:
        assetClasses = ueConfig.Config(spec).config["assetClasses"]

    append = ""
    if "pathappend" in assetClasses[spec.elclass]:
        append = parsePath(assetClasses[spec.elclass]["pathappend"], vers=int(spec.vers))

    elpass = ""
    if not spec.elpass == None:
        elpass = spec.elpass

    return os.path.join(getElementPath(spec, assetClasses=assetClasses), append, elpass)


def getElementName(spec):
    s = "%s_%s_%s_%s_%s_%s_%04d" % (spec.proj, spec.grp, spec.asst,
                                    spec.elname, spec.eltype,
                                    spec.elclass, int(spec.vers))
    if not spec.elpass == None:
        s = "%s_%s" % (s, spec.elpass)
    return s


def getThumbnailPath(spec):
    p =  os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, getElementName(spec)+".png")
    if not os.path.exists(p):
        p = os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png")
    return p

