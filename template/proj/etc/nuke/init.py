import ueClient

import ueNuke
import ueNuke.Load as ueNukeLoad

ueClient.Client()

nuke.pluginAddPath(ueNukeLoad.loadGizmos())

# Utilities
def getReadPath():
    return ueNuke.getReadPath()

def getReadGeoPath():
    return ueNuke.getReadGeoPath()

