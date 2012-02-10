"""Returns information on ue assets and elements

Read-only functions for returning information on ue
assets and elements.
"""

import os

import ueClient, ueSpec

import ueCore.Config as ueConfig

def getProject(spec):
    """Returns a project dictionary
    """
    return ueClient.client.getProject(spec)

def getProjectsList():
    """Returns a string of project dictionaries
    """
    projects = []
    for p in ueClient.client.getProjects():
        projects.append(p["name"])
    return projects


def getGroup(spec):
    """Returns a group dictionary
    """
    return ueClient.client.getGroup(spec)

def getGroupsList(spec):
    """Returns a list of group dictionaries
    """
    groups = []
    for g in ueClient.client.getGroups(spec):
        groups.append(g["name"])
    return groups


def getAsset(spec):
    """Returns an asset dictionary
    """
    return ueClient.client.getAsset(spec)

def getAssetsList(spec):
    """Returns a list of asset dictionaries
    """
    assets = []
    for a in ueClient.client.getAssets(spec):
        assets.append(a["name"])
    return assets


def getElement(spec):
    """Returns a formatted dictionary of a single
       element
    """
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
    """Returns a formatted dictionary with all the
       elements in an asset
    """
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
    """Returns a list of versions
    """
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
    """String replacement operations on paths

       kwargs is a dictionary of arguments to
       parse
    """
    p = path
    if "vers" in kwargs:
        p = path.replace("%%version%%", "%04d" % kwargs["vers"])
    return p

def getElementPath(spec, assetClasses=None):
    """Returns the absolute path of a given element
    """
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
    """Returns the absolute path of a given version
       of a given element
    """
    if assetClasses == None:
        assetClasses = ueConfig.Config(spec).config["assetClasses"]

    append = ""
    if "pathappend" in assetClasses[spec.elclass]:
        append = parsePath(assetClasses[spec.elclass]["pathappend"], vers=spec.vers)

    return os.path.join(getElementPath(spec, assetClasses=assetClasses), append)


def getElementName(spec):
    """Returns the file name of a version of a given
       element without a file extension
    """
    try:
        s = "%s_%s_%s_%s_%s_%s_%04d" % (spec.proj, spec.grp, spec.asst,
                                        spec.elname, spec.eltype,
                                        spec.elclass, spec.vers)
    except TypeError:
        s = "%s_%s_%s_%s_%s_%s_%s" % (spec.proj, spec.grp, spec.asst,
                                      spec.elname, spec.eltype,
                                      spec.elclass, spec.vers)
    return s


def getThumbnailPath(spec):
    """Returns the absolute thumbnail path of a given
       asset/element/version. If the thumbnail image
       doesn't exist, a default placeholder image is
       returned.
    """
    p =  os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, getElementName(spec)+".png")
    if not os.path.exists(p):
        p = os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png")
    return p
