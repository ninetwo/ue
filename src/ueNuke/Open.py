import os

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCommon.Open as ueCommonOpen

def ueOpen():
    p = nukescripts.registerWidgetAsPanel("ueCommonOpen.Open", "ueOpen",
                                          "ue.panel.ueOpen", create=True)
    p.setMinimumSize(600, 920)
    ueCommonOpen.setClasses(["c"])

    if p.showModalDialog():
        spec = ueCommonOpen.getValues()
        nkPath = ueAssetUtils.getVersionPath(spec)
        nkFile = ueAssetUtils.getElementName(spec)
        nuke.scriptOpen(os.path.join(nkPath, nkFile+".nk"))
        nuke.tprint("Opened %s" % spec)

    nukescripts.unregisterPanel("ue.panel.ueOpen", lambda: "return")

