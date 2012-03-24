import os, sys
import time, getpass

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

def createProject(spec, dbMeta={}):
    project = {}

    project["name"] = spec.proj
    project["created_by"] = getpass.getuser()

    for m in dbMeta:
        project[m] = dbMeta[m]

    ueClient.client.saveProject(spec, project)

    return ueAssetUtils.getProject(spec)

def createGroup(spec, grpType="default", dbMeta={}):
    group = {}

    group["name"] = spec.grp
    group["group_type"] = grpType
    group["created_by"] = getpass.getuser()

    for m in dbMeta:
        group[m] = dbMeta[m]

    ueClient.client.saveGroup(spec, group)

    return ueAssetUtils.getGroup(spec)

def createAsset(spec, asstType="default", dbMeta={}):
    asset = {}

    asset["name"] = spec.asst
    asset["asset_type"] = asstType
    asset["created_by"] = getpass.getuser()

    for m in dbMeta:
        asset[m] = dbMeta[m]

    ueClient.client.saveAsset(spec, asset)

    return ueAssetUtils.getAsset(spec)

def createElement(spec, dbMeta={}):
    element = {}

    element["created_by"] = getpass.getuser()

    for m in dbMeta:
        element[m] = dbMeta[m]

    ueClient.client.saveElement(spec, element)

    return ueAssetUtils.getElement(spec)

def createVersion(spec, dbMeta={}, layer=None):
    version = {}

    spec.vers = len(ueAssetUtils.getVersions(spec))+1

    version["version"] = spec.vers
    version["created_by"] = getpass.getuser()

    for m in dbMeta:
        version[m] = dbMeta[m]

    if not layer == None:
        p = os.path.join(version["path"])

    ueClient.client.saveVersion(spec, version)

    return ueAssetUtils.getVersions(spec)[spec.vers-1]

