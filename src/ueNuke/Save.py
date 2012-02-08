import os, sys

from PyQt4 import QtGui

import nuke, nukescripts

import ueSpec

import ueCore.FileUtils as ueFileUtils

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

    app = QtGui.QApplication.allWidgets()
    i = 0
    for widget in app:
        if str(type(widget)) == "<class 'PyQt4.QtGui.QStackedWidget'>":
            name = "ueSaveThumbs_%04d.png" % i
            QtGui.QPixmap.grabWindow(widget.winId()).save(os.path.join(os.getenv("ASST_ROOT"), "tmp", name), "png")
            i += 1

    p = nukescripts.registerWidgetAsPanel("ueCommonSave.Save", "ueSave",
                                          "ue.panel.ueSave", create=True)
    p.setMinimumSize(400, 600)
    ueCommonSave.setClasses(["c"])

    if p.showModalDialog():
        spec = ueCommonSave.getValues()
        ueNukeUtils.saveUtility(spec)

    ueFileUtils.deleteFiles(os.path.join(os.path.join(os.getenv("ASST_ROOT"), "tmp", "ueSaveThumbs_*.png")))
    nukescripts.unregisterPanel("ue.panel.ueSave", lambda: "return")

