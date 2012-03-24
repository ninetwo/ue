import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

def destroyProject(spec):
    ueClient.client.destroyProject(spec)

def destroyGroup(spec):
    ueClient.client.destroyGroup(spec)

def destroyAsset(spec):
    ueClient.client.destroyAsset(spec)

def destroyElement(spec):
    ueClient.client.destroyElement(spec)

def destroyVersion(spec):
    ueClient.client.destroyVersion(spec)

