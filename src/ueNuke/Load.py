import os, glob

import nuke

import ueSpec

import ueCore.AssetUtils as ueAssetUtils

proj = os.getenv("PROJ")
grp = os.getenv("GRP")
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
    print "add"

def loadGizmosFromAsset(asst):
    path = []
    a = ueAssetUtils.getElements(ueSpec.Spec(asst[0], asst[1], asst[2]))
    if "giz" in a:
        for n in a["giz"]:
            for p in a["giz"][n]:
                path.append(a["giz"][n][p]["path"])
    return path

def addGizmosFromAsset(asst):
    a = ueAssetUtils.getElements(ueSpec.Spec(asst[0], asst[1], asst[2]))
    if "giz" in a:
        for n in a["giz"]:
            for p in a["giz"][n]:
                spec = ueSpec.Spec(asst[0], asst[1], asst[2], "giz", n, p)
                vers = ueAssetUtils.getVersions(spec)
                gizName = ueAssetUtils.getElementName(spec)
                menu = "%s:%s:%s/%s/%s" % (spec.proj, spec.grp, spec.asst, n, p)
                # Add a 'ueGizVers' knob to hold the version of the gizmo
                # we're bringing in. This can be used for version control later.
                # When you add a custom knob, Nuke makes the User tab active,
                # so a hack around that is to add the node with the prefs panel
                # disabled, add the custom knobs, then show the prefs.
                command =  str('n = nuke.createNode("'+gizName+'", "name '+p+'", \
                           inpanel=False); \
                           n.addKnob(nuke.Int_Knob("ueGizmoVers", "gizmo version")); \
                           n.knob("ueGizmoVers").setValue('+str(len(vers))+'); \
                           n.showControlPanel()')
                nuke.toolbar("Nodes").addCommand("ueTools/"+menu, command)
                nuke.menu("Nuke").addCommand("ueTools/gizmos/"+menu, command)

