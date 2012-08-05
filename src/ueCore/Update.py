import os, sys
import time, getpass

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

def updateProject(spec, dbMeta={}):
    ueClient.client.updateProject(spec, dbMeta)

    return ueAssetUtils.getProject(spec)

def updateGroup(spec, grpType="default", dbMeta={}):
    ueClient.client.updateGroup(spec, dbMeta)

    return ueAssetUtils.getGroup(spec)

def updateAsset(spec, asstType="default", dbMeta={}):
    ueClient.client.updateAsset(spec, dbMeta)

    return ueAssetUtils.getAsset(spec)

def updateElement(spec, dbMeta={}):
    ueClient.client.updateElement(spec, dbMeta)

    return ueAssetUtils.getElement(spec)

def updateVersion(spec, dbMeta={}):
    spec.vers = len(ueAssetUtils.getVersions(spec))+1

    ueClient.client.updateVersion(spec, dbMeta)

    return ueAssetUtils.getVersions(spec)[spec.vers-1]

