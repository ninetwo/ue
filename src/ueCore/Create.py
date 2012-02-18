import os, sys
import time, getpass

import ueClient, ueSpec

import ueCore.Config as ueConfig
import ueCore.AssetUtils as ueAssetUtils
import ueCore.FileUtils as ueFileUtils

def createProject(spec, dbMeta={}):
    project = {}

    project["name"] = spec.proj
    project["created_by"] = getpass.getuser()

    for m in dbMeta:
        project[m] = dbMeta[m]

    ueClient.client.saveProject(spec, project)

    return project

def createGroup(spec, grpType="default", dbMeta={}):
    group = {}

    group["name"] = spec.grp
    group["group_type"] = grpType
    group["created_by"] = getpass.getuser()

    for m in dbMeta:
        group[m] = dbMeta[m]

    ueClient.client.saveGroup(spec, group)

    return group

def createAsset(spec, asstType="default", dbMeta={}):
    asset = {}

    asset["name"] = spec.asst
    asset["asset_type"] = asstType
    asset["created_by"] = getpass.getuser()

    for m in dbMeta:
        asset[m] = dbMeta[m]

    ueClient.client.saveAsset(spec, asset)

    return asset

def createElement(spec, dbMeta={}):
    element = {}

#    element["path"] = ueAssetUtils.getElementPath(spec)
    element["created_by"] = getpass.getuser()

    for m in dbMeta:
        element[m] = dbMeta[m]

    ueClient.client.saveElement(spec, element)
#    ueFileUtils.createDir(element["path"])

    return element

def createVersion(spec, dbMeta={}, layer=None):
    version = {}

    spec.vers = len(ueAssetUtils.getVersions(spec))+1

    version["version"] = spec.vers
#    version["path"] = ueAssetUtils.getVersionPath(spec)
    version["created_by"] = getpass.getuser()

    for m in dbMeta:
        version[m] = dbMeta[m]

    if not layer == None:
        p = os.path.join(version["path"])

    ueClient.client.saveVersion(spec, version)
#    ueFileUtils.createDir(version["path"])

    return version

