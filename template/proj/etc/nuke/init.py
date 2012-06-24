import ueClient

import ueNuke
import ueNuke.Load as ueNukeLoad

ueClient.Client()

nuke.pluginAddPath(ueNukeLoad.loadGizmos())

# Auto-run
nuke.addOnUserCreate(ueNuke.ueNewScriptSetup, nodeClass="Root")

# Utilities
def getReadPath():
    return ueNuke.getReadPath()

def getReadGeoPath():
    return ueNuke.getReadGeoPath()

def ueReadAsset(node, cmd=None, name=None):
    return ueNuke.ueReadAsset(node, cmd=cmd, name=name)

def ueWriteAsset(node, cmd=None, name=None):
    return ueNuke.ueWriteAsset(node, cmd=cmd, name=name)

