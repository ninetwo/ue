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
    project["created_at"] = time.time()
    project["project_dirs"] = config.projectDirs
    project["group_dirs"] = config.groupDirs
    project["asset_dirs"] = config.assetDirs
    project["asset_classes"] = config.assetClasses
    project["asset_settings"] = config.assetSettings

    ueClient.client.saveProject(spec, project)
    ueFileUtils.createDirTree(project["path"], config.projectDirs)

    return project

def createGroup(spec, grpType="default"):
    group = {}

    config = ueConfig.Config(spec).config.groupDirs[grpType]

    project = ueAssetUtils.getProject(spec)

    group["name"] = spec.grp
    group["path"] = os.path.join(project["path"], config[1], spec.grp)
    group["type"] = grpType
    group["created_by"] = getpass.getuser()
    group["created_at"] = time.time()

    ueClient.client.saveGroup(spec, group)
    ueFileUtils.createDirTree(group["path"], config[0])

    return group

def createAsset(spec, asstType="default"):
    asset = {}

    config = ueConfig.Config(spec).config.assetDirs[asstType]

    group = ueAssetUtils.getGroup(spec)

    asset["name"] = spec.asst
    asset["group"] = spec.grp
    asset["path"] = os.path.join(group["path"], config[1], spec.asst)
    asset["type"] = asstType
    asset["created_by"] = getpass.getuser()
    asset["created_at"] = time.time()

    ueClient.client.saveAsset(spec, asset)
    ueFileUtils.createDirTree(asset["path"], config[0])

    return asset

def createElement(spec):
    element = {}

    element["path"] = ueAssetUtils.getElementPath(spec)
    element["created_by"] = getpass.getuser()
    #element["created_at"] = time.time()

    ueClient.client.saveElement(spec, element)
    #ueFileUtils.createDir(element["path"])

    return element

def createVersion(spec, **kwargs):
    version = {}

    version["version"] = len(ueAssetUtils.getVersions(spec))+1
    version["path"] = ueAssetUtils.getVersionPath(spec)
    version["created_by"] = getpass.getuser()
    #version["created_at"] = time.time()

    ueClient.client.saveVersion(spec, version)
    #ueFileUtils.createDir(version["path"])

    return version

