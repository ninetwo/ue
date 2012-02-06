import nuke, nukescripts

import ueSpec

import ueNuke
import ueNuke.Utilities as ueNukeUtils
import ueCommon.Save as ueCommonSave

elclass = "c"

def ueSave():
    root = nuke.root()

    if root.name() == "Root":
        ueSaveAs()
        return

#    if not ueNuke.ueScriptSanityCheck():
#        return

    nuke.scriptSave(root.knob("name").value())

def ueSaveVers(**kargs):
    root = nuke.root()

    if root.name() == "Root":
        ueSaveAs()
        return

#    if not ueNuke.ueScriptSanityCheck():
#        return

    spec = ueSpec.Spec(root.knob("proj").value(),
                       root.knob("grp").value(),
                       root.knob("asst").value(),
                       elclass,
                       root.knob("uetype").value(),
                       root.knob("uename").value())

    ueNukeUtils.saveUtility(spec)

def ueSaveAs():
#    if not ueNuke.ueScriptSanityCheck():
#        return

    p = nukescripts.registerWidgetAsPanel("ueCommonSave.Save", "ueSave",
                                          "ue.panel.ueSave", create=True)
    p.setMinimumSize(400, 500)
    ueCommonSave.setClasses(["c"])

    if p.showModalDialog():
        spec = ueCommonSave.getValues()
        ueNukeUtils.saveUtility(spec)

    nukescripts.unregisterPanel("ue.panel.ueSave", lambda: "return")

