import os, sys

import nuke, nukescripts

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

import ueNuke
import ueNuke.Utilities as ueNukeUtils

__CLASS__ = "c"

def ueSave():
    if nuke.root().name() == "Root":
        ueSaveAs()
        return

    if not ueNuke.ueScriptSanityCheck():
        return

    nuke.scriptSave(nuke.root().knob("name").value())

def ueSaveVers():
    root = nuke.root()

    if root.name() == "Root":
        ueSaveAs()
        return

    if not ueNuke.ueScriptSanityCheck():
        return

    proj = root.knob("proj").value()
    grp = root.knob("grp").value()
    asst = root.knob("asst").value()
    elclass = __CLASS__
    eltype = root.knob("uetype").value()
    name = root.knob("uename").value()

    ueNukeUtils.saveUtility(proj, grp, asst, elclass, eltype, name)

def ueSaveAs():
    if not ueNuke.ueScriptSanityCheck():
        return

    p = UeSavePanel()
    p.setMinimumSize(400, 100)

    if p.showModalDialog():
        proj = p.proj
        grp = p.grp
        asst = p.asst
        elclass = p.elclass
        eltype = p.eltype
        name = p.name

        ueNukeUtils.saveUtility(proj, grp, asst, elclass, eltype, name)


class UeSavePanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "Save script")

        self.proj = os.getenv("PROJ")
        self.grp = os.getenv("GROUP")
        self.asst = os.getenv("ASST")
        self.elclass = __CLASS__
        self.eltype = None
        self.name = None

        root = nuke.root()

        if not root.knob("uetype") == None:
            self.eltype = root.knob("uetype").value()

        na = []
        if not root.knob("uename") == None:
            self.name = root.knob("uename").value()
            na = ueAssetUtils.getNamesList(self.proj, self.grp, self.asst, self.elclass, self.eltype)

        self.elKnobs = []
        self.elStrKnobs = []
        self.elKnobs.append(nuke.Enumeration_Knob("proj", "project",
                            ueAssetUtils.getProjectsList()))
        self.elKnobs.append(nuke.Enumeration_Knob("grp", "group",
                            ueAssetUtils.getGroupsList(self.proj)))
        self.elKnobs.append(nuke.Enumeration_Knob("asst", "asset",
                            ueAssetUtils.getAssetsList(self.proj, self.grp)))
        self.elKnobs.append(nuke.Enumeration_Knob("type", "type",
                            ueAssetUtils.getTypesList(self.proj, self.grp, self.asst, self.elclass)))
        self.elKnobs.append(nuke.nuke.String_Knob("newtype", ""))
        self.elKnobs[-1].clearFlag(nuke.STARTLINE)
        self.elKnobs.append(nuke.Enumeration_Knob("name", "name", na))
        self.elKnobs.append(nuke.nuke.String_Knob("newname", ""))
        self.elKnobs[-1].clearFlag(nuke.STARTLINE)

        for k in self.elKnobs:
            self.addKnob(k)

        self.elKnobs[0].setValue(self.proj)
        self.elKnobs[1].setValue(self.grp)
        self.elKnobs[2].setValue(self.asst)
        if not self.eltype == None:
            self.elKnobs[3].setValue(self.eltype)
        if not self.name == None:
            self.elKnobs[5].setValue(self.name)

        self.knobChanged(self.elKnobs[0])

    def knobChanged(self, knob):
        if knob in self.elKnobs:
            t = []
            idx = 1
            if knob == self.elKnobs[0]:
                self.proj = self.elKnobs[0].value()
                self.elKnobs[1].setEnabled(True)
                t = ueAssetUtils.getGroupsList(self.proj)
                self.elKnobs[1].setValues(t)
                idx = 2
            if knob == self.elKnobs[1] or not t == []:
                self.grp = self.elKnobs[1].value()
                self.elKnobs[2].setEnabled(True)
                t = ueAssetUtils.getAssetsList(self.proj, self.grp)
                self.elKnobs[2].setValues(t)
                idx = 3
            if knob == self.elKnobs[2] or not t == []:
                self.asst = self.elKnobs[2].value()
                self.elKnobs[3].setEnabled(True)
                t = ueAssetUtils.getTypesList(self.proj, self.grp, self.asst, self.elclass)
                self.elKnobs[3].setValues(t)
                idx = 4
            if knob == self.elKnobs[3] or not t == []:
                self.eltype = self.elKnobs[3].value()
                self.elKnobs[5].setEnabled(True)
                t = ueAssetUtils.getNamesList(self.proj, self.grp, self.asst, self.elclass, self.eltype)
                self.elKnobs[5].setValues(t)
                idx = 5
            if knob == self.elKnobs[4]:
                self.eltype = self.elKnobs[4].value()
                idx = 6
            if knob == self.elKnobs[5] or not t == []:
                self.name = self.elKnobs[5].value()
                self.elKnobs[6].setEnabled(True)
                idx = 7
            if knob == self.elKnobs[6]:
                self.name = self.elKnobs[6].value()
                idx = 8

            for n in range(idx, len(self.elKnobs)):
                if not n in [4, 6]:
                    self.elKnobs[n].setEnabled(False)
                    self.elKnobs[n].setValues([])

