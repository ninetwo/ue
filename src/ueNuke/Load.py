import os, glob

import nuke

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

proj = os.getenv("PROJ")
grp = os.getenv("GROUP")
asst = os.getenv("ASST")

# List of assets to scan for gizmos and scriptlets
libs = [(proj, "lib", "global"),
        (proj, grp, "global"),
        (proj, grp, asst)]

def loadGizmos():
    path = []
    for l in libs:
        path += loadGizmosFromAsset(l)
    return path

def addGizmos():
    for l in libs:
        addGizmosFromAsset(l)

def loadGizmosFromAsset(asst):
    path = []
    a = ueAssetUtils.getElements(asst[0], asst[1], asst[2])
    if "giz" in a:
        for n in a["giz"]:
            for p in a["giz"][n]:
                path.append(a["giz"][n][p]["path"])
    return path

def addGizmosFromAsset(asst):
    a = ueAssetUtils.getElements(asst[0], asst[1], asst[2])
    if "giz" in a:
        for n in a["giz"]:
            for p in a["giz"][n]:
                vers = ueAssetUtils.getVersions(asst[0], asst[1], asst[2],
                                                "giz", n, p)
                gizName = ueCreateUtils.getElementName(asst[0], asst[1], asst[2],
                                                       "giz", n, p, len(vers))
                menu = asst[0]+":"+asst[1]+":"+asst[2]+"/"+n+"/"+p
                command =  str('n = nuke.createNode("'+gizName+'", "name '+p+'"); \
                           n.addKnob(nuke.Int_Knob("ueGizmoVers", "gizmo version")); \
                           n.knob("ueGizmoVers").setValue('+str(len(vers))+')')
                nuke.toolbar("Nodes").addCommand("ueTools/"+menu, command)
                nuke.menu("Nuke").addCommand("ueTools/gizmos/"+menu, command)

