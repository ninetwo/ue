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
    return sorted(projects)


def getGroup(spec):
    return ueClient.client.getGroup(spec)

def getGroups(spec):
    return ueClient.client.getGroups(spec)

def getGroupsList(spec):
    groups = []
    for g in ueClient.client.getGroups(spec):
        groups.append(g["name"])
    return sorted(groups)


def getAsset(spec):
    return ueClient.client.getAsset(spec)

def getAssets(spec):
    return ueClient.client.getAssets(spec)

def getAssetsList(spec):
    assets = []
    for a in ueClient.client.getAssets(spec):
        assets.append(a["name"])
    return sorted(assets)


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
#        if "comment" in e:
#            elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["comment"] = e["comment"]       
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
        for el in e:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]][el] = e[el]
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
#        if "comment" in e:
#            elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["comment"] = e["comment"]
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["path"] = e["path"]
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_at"] = e["created_at"]
#        elementsDict[e["elclass"]][e["eltype"]][e["elname"]]["created_by"] = e["created_by"]
        for el in e:
            elementsDict[e["elclass"]][e["eltype"]][e["elname"]][el] = e[el]
    return elementsDict


def getVersion(spec):
    versions = getVersions(spec)
    if spec.vers == None:
        spec.vers = -1
    elif not spec.vers < 0:
        spec.vers -= 1
    if spec.vers >= len(versions):
        return []
    else:
        return versions[spec.vers]

def getVersions(spec):
    element = ueClient.client.getElement(spec)
    if not "versions" in element:
        element["versions"] = []
    return element["versions"]


def getThumbnailPath(spec):
#    p =  os.path.join(os.getenv("PROJ_ROOT"), "var", "thumbs", spec.grp, spec.asst, getElementName(spec)+".png")
#    if not os.path.exists(p):
    p = os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "thumbnail.png")
    return p

