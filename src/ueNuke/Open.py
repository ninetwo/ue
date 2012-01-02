import os, sys
import re, glob

import nuke, nukescripts

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

def ueOpen():
    p = UeOpenPanel()

    if p.showModalDialog():
        if p.selectedScript:
            nuke.scriptOpen(p.selectedScript)

def getScriptsList(proj, grp, asst, elclass, eltype, name):
    nkVers = []
    e = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    f = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, "*")
    if not e == None:
        nkFiles = glob.glob(os.path.join(e["path"], f+".nk"))
        for f in nkFiles:
            nkVers.append(re.split("([0-9]{3})", f)[-2])
    return sorted(nkVers, reverse=True)

def getNukeScript(proj, grp, asst, elclass, eltype, name, vers):
    nkFile = ""
    e = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    if not e == None:
        nkFile = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, vers)
        f = glob.glob(os.path.join(e["path"], nkFile+".nk"))
        if not f == []:
            nkFile = f[0]
    return nkFile

class UeOpenPanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "Open script")
        self.selectedScript = None

        self.proj = os.getenv("PROJ")
        self.grp = os.getenv("GROUP")
        self.asst = os.getenv("ASST")
        self.elclass = "c"
        self.eltype = None
        self.name = None
        self.vers = None

        root = nuke.root()

        ty = []
        if not root.knob("uetype") == None:
            self.eltype = root.knob("uetype").value()
            ty = ueAssetUtils.getTypesList(self.proj, self.grp, self.asst, self.elclass)

        na = []
        if not root.knob("uename") == None:
            self.name = root.knob("uename").value()
            na = ueAssetUtils.getNamesList(self.proj, self.grp, self.asst, self.elclass, self.eltype)

        self.elKnobs = []
        self.elKnobs.append(nuke.Enumeration_Knob("proj", "project",
                            ueAssetUtils.getProjectsList()))
        self.elKnobs.append(nuke.Enumeration_Knob("grp", "group",
                            ueAssetUtils.getGroupsList(self.proj)))
        self.elKnobs.append(nuke.Enumeration_Knob("asst", "asset",
                            ueAssetUtils.getAssetsList(self.proj, self.grp)))
        self.elKnobs.append(nuke.Enumeration_Knob("type", "type", ty))
        self.elKnobs.append(nuke.Enumeration_Knob("name", "name", na))
        self.elKnobs.append(nuke.Enumeration_Knob("vers", "version", []))

        for k in self.elKnobs:
            self.addKnob(k)

        self.elKnobs[0].setValue(self.proj)
        self.elKnobs[1].setValue(self.grp)
        self.elKnobs[2].setValue(self.asst)
        if not self.eltype == None:
            self.elKnobs[3].setValue(self.eltype)
        if not self.name == None:
            self.elKnobs[4].setValue(self.name)

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
                self.elKnobs[4].setEnabled(True)
                t = ueAssetUtils.getNamesList(self.proj, self.grp, self.asst, self.elclass, self.eltype)
                self.elKnobs[4].setValues(t)
                idx = 5
            if knob == self.elKnobs[4] or not t == []:
                self.name = self.elKnobs[4].value()
                self.elKnobs[5].setEnabled(True)
                t = getScriptsList(self.proj, self.grp, self.asst, self.elclass, self.eltype, self.name)
                self.elKnobs[5].setValues(t)
                idx = 6
            if knob == self.elKnobs[5] or not t == []:
                self.vers = int(self.elKnobs[5].value())
                self.selectedScript = getNukeScript(self.proj, self.grp, self.asst, self.elclass, self.eltype, self.name, self.vers)
                idx = 7

            for n in range(idx, len(self.elKnobs)):
                self.elKnobs[n].setEnabled(False)
                self.elKnobs[n].setValues([])

