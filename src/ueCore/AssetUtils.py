import os, sys
import json

import ueCore.Settings as ueSettings
import ueCore.ConfigUtils as ueConfigUtils

def getProjects():
    projects = {}

    if os.path.exists(ueSettings.__UE_PROJ_FILE_PATH__):
        f = open(ueSettings.__UE_PROJ_FILE_PATH__, 'r')
        projects = json.loads(f.read())
        f.close()

    return projects

def getProject(proj):
    projects = getProjects()

    p = None
    if proj in projects:
        p = projects[proj]

    return p

def getProjectsList():
    projects = getProjects()

    projectsList = []
    for p in projects:
        projectsList.append(p)

    return projectsList


def getGroups(proj):
    project = getProject(proj)

    if project == None:
        return {}

    projGroups = os.path.join(project["path"], "etc", "groups")

    groups = {}
    if os.path.exists(projGroups):
        f = open(projGroups, 'r')
        groups = json.loads(f.read())
        f.close()

    return groups

def getGroup(proj, grp):
    groups = getGroups(proj)

    g = None
    if grp in groups:
        g = groups[grp]

    return g

def getGroupsList(proj):
    groups = getGroups(proj)

    groupsList = []
    for g in groups:
        groupsList.append(g)

    return groupsList


def getAssets(proj, grp):
    group = getGroup(proj, grp)

    if group == None:
        return {}

    groupAssets = os.path.join(group["path"], "etc", "assets")

    assets = {}
    if os.path.exists(groupAssets):
        f = open(groupAssets, 'r')
        assets = json.loads(f.read())
        f.close()

    return assets

def getAsset(proj, grp, asst):
    assets = getAssets(proj,   grp)

    a = None
    if asst in assets:
        a = assets[asst]

    return a

def getAssetsList(proj, grp):
    assets = getAssets(proj, grp)

    assetsList = []
    for a in assets:
        assetsList.append(a)

    return assetsList


def getClasses(proj, grp, asst):
    asset = getAsset(proj, grp, asst)

    if asset == None:
        return {} 

    #classes = ueConfigUtils.getConfig(proj, grp, asst)["ASSET_CLASSES"]
    assetClasses = os.path.join(asset["path"], "etc", "elements")

    classes = {}
    if os.path.exists(assetClasses):
        f = open(assetClasses, "r")
        classes = json.loads(f.read())
        f.close()

    return classes

def getClass(proj, grp, asst, elclass):
    classes = getClasses(proj, grp, asst)

    c = None
    if elclass in classes:
        c = classes[elclass]

    return c

def getClassesList(proj, grp, asst):
    classes = getClasses(proj, grp, asst)

    classesList = []
    for c in classes:
        classesList.append(c)

    return classesList


def getTypesList(proj, grp, asst, elclass):
    asstClass = getClass(proj, grp, asst, elclass)

    if asstClass == None:
        return []

    typesList = []
    for c in asstClass:
        typesList.append(c)

    return typesList


def getNames(proj, grp, asst, elclass, eltype):
    asset = getAsset(proj, grp, asst)

    if asset == None:
        return {}

    assetElements = os.path.join(asset["path"], "etc", "elements")

    elements = {}
    if os.path.exists(assetElements):
        f = open(assetElements, "r")
        elements = json.loads(f.read())
        f.close()

    names = {}
    if elclass in elements:
        if eltype in elements[elclass]:
            names = elements[elclass][eltype]

    return names

def getNamesList(proj, grp, asst, elclass, eltype):
    names = getNames(proj, grp, asst, elclass, eltype)

    namesList = []
    for n in names:
        namesList.append(n)

    return namesList


def getElements(proj, grp, asst):
    asset = getAsset(proj, grp, asst)

    if asset == None:
        return {}

    assetElements = os.path.join(asset["path"], "etc", "elements")

    elements = {}
    if os.path.exists(assetElements):
        f = open(assetElements, "r")
        elements = json.loads(f.read())
        f.close()

    return elements

def getElement(proj, grp, asst, elclass, eltype, name):
    elements = getElements(proj, grp, asst)

    e = None
    if elclass in elements:
        if eltype in elements[elclass]:
            if name in elements[elclass][eltype]:
                e = elements[elclass][eltype][name]

    return e

def getElementsList(proj, grp, asst, elclass):
    elements = getElements(proj, grp, asst, elclass)

    elementsList = []
    for e in elements:
        elementsList.append(e)

    return elementsList

def getVersions(proj, grp, asst, elclass, eltype, name):
    element = getElement(proj, grp, asst, elclass, eltype, name)

    if element == None:
        return []

    elementVersions = os.path.join(element["path"], "versions")

    versions = []
    if os.path.exists(elementVersions):
        f = open(elementVersions, "r")
        versions = json.loads(f.read())
        f.close()

    return versions

