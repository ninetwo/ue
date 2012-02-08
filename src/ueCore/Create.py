import os, sys
import time, getpass

import ueClient, ueSpec

import ueCore.Config as ueConfig
import ueCore.AssetUtils as ueAssetUtils
import ueCore.FileUtils as ueFileUtils

def createProject(spec):
    project = {}

    config = ueConfig.Config().config

    project["name"] = spec.proj
    project["path"] = os.path.join("/work", spec.proj)
    project["created_by"] = getpass.getuser()

    ueClient.client.saveProject(spec, project)
    ueClient.client.saveConfig(spec, config)
    ueFileUtils.createDirTree(project["path"], config["projectDirs"])

    return project

def createGroup(spec, grpType="default", confOverrides=None):
    group = {}

    config = ueConfig.Config(spec).config["groupDirs"][grpType]

    project = ueAssetUtils.getProject(spec)

    group["name"] = spec.grp
    group["path"] = os.path.join(project["path"], config[1], spec.grp)
    group["type"] = grpType
    group["created_by"] = getpass.getuser()

    ueClient.client.saveGroup(spec, group)
    ueFileUtils.createDirTree(group["path"], config[0])

    return group

def createAsset(spec, asstType="default", confOverrides=None):
    asset = {}

    config = ueConfig.Config(spec).config["assetDirs"][asstType]

    group = ueAssetUtils.getGroup(spec)

    asset["name"] = spec.asst
    asset["group"] = spec.grp
    asset["path"] = os.path.join(group["path"], config[1], spec.asst)
    asset["type"] = asstType
    asset["created_by"] = getpass.getuser()

    ueClient.client.saveAsset(spec, asset)
    if not confOverrides == None:
        ueClient.client.saveConfig(spec, confOverrides)
    ueFileUtils.createDirTree(asset["path"], config[0])

    return asset

def createElement(spec, dbMeta={}):
    element = {}

    element["path"] = ueAssetUtils.getElementPath(spec)
    element["created_by"] = getpass.getuser()

    for m in dbMeta:
        element[m] = dbMeta[m]

    ueClient.client.saveElement(spec, element)
    ueFileUtils.createDir(element["path"])

    return element

def createVersion(spec, dbMeta={}):
    version = {}

    version["version"] = len(ueAssetUtils.getVersions(spec))+1
    version["path"] = ueAssetUtils.getVersionPath(spec)
    version["created_by"] = getpass.getuser()

    for m in dbMeta:
        version[m] = dbMeta[m]

    ueClient.client.saveVersion(spec, version)
    ueFileUtils.createDir(version["path"])

    return version

