import os, sys
import re, glob

import nuke, nukescripts

import ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.Config as ueConfig

checker = \
{
 "nuke": {
          "Framerate":  {
                         "desc": "Framerate",
                         "eval": "float(nuke.root().knob(\"fps\").value()) != float(os.getenv(\"FRAMERATE\"))",
                         "update": "nuke.root().knob(\"fps\").setValue(float(os.getenv(\"FRAMERATE\")))",
                         "curval": "float(nuke.root().knob(\"fps\").value())",
                         "newval": "float(os.getenv(\"FRAMERATE\"))"
                        },
          "Start Frame": {
                         "desc": "Start frame",
                         "eval": "float(nuke.root().knob(\"first_frame\").value()) != float(os.getenv(\"STARTFRAME\"))",
                         "update": "nuke.root().knob(\"first_frame\").setValue(float(os.getenv(\"STARTFRAME\")))",
                         "curval": "float(nuke.root().knob(\"first_frame\").value())",
                         "newval": "float(os.getenv(\"STARTFRAME\"))"
                        },
          "End Frame": {
                         "desc": "End frame",
                         "eval": "float(nuke.root().knob(\"last_frame\").value()) != float(os.getenv(\"ENDFRAME\"))",
                         "update": "nuke.root().knob(\"last_frame\").setValue(float(os.getenv(\"ENDFRAME\")))",
                         "curval": "float(nuke.root().knob(\"last_frame\").value())",
                         "newval": "float(os.getenv(\"ENDFRAME\"))"
                       }
        },
 "test": {
         "Project":    {
                        "desc": "Project",
                        "eval": "nuke.root.knob(\"proj\").value() != os.getenv(\"PROJ\")",
                        "update": "nuke.root().knob(\"proj\").setValue(os.getenv(\"PROJ\"))",
                        "curval": "nuke.root().knob(\"proj\").value()",
                        "newval": "os.getenv(\"PROJ\")"
                       },
         "Group":    {
                        "desc": "Group",
                        "eval": "nuke.root.knob(\"grp\").value() != os.getenv(\"GROUP\")",
                        "update": "nuke.root().knob(\"grp\").setValue(os.getenv(\"GROUP\"))",
                        "curval": "nuke.root().knob(\"grp\").value()",
                        "newval": "os.getenv(\"GROUP\")"
                       },
         "Asset":    {
                        "desc": "Asset",
                        "eval": "nuke.root.knob(\"asst\").value() != os.getenv(\"ASST\")",
                        "update": "nuke.root().knob(\"asst\").setValue(os.getenv(\"ASST\"))",
                        "curval": "nuke.root().knob(\"asst\").value()",
                        "newval": "os.getenv(\"ASST\")"
                       },
         "Asset Root":    {
                        "desc": "Asset Root",
                        "eval": "nuke.root.knob(\"asst_root\").value() != os.getenv(\"ASST_ROOT\")",
                        "update": "nuke.root().knob(\"asst_root\").setValue(os.getenv(\"ASST_ROOT\"))",
                        "curval": "nuke.root().knob(\"asst_root\").value()",
                        "newval": "os.getenv(\"ASST_ROOT\")"
                       },
        }
}

def ueNewScriptSetup():
    root = nuke.root()

    spec = ueSpec.Spec(os.getenv("PROJ"),
                       os.getenv("GRP"),
                       os.getenv("ASST"))

    config = ueConfig.Config(spec).config["assetSettings"]

    formatName = "ueProjectRes"

    root.knob("fps").setValue(int(config["frameRate"]))
    root.knob("first_frame").setValue(int(config["startFrame"]))
    root.knob("last_frame").setValue(int(config["endFrame"]))

    x = int(config["xRes"])+int(config["xPad"])
    y = int(config["yRes"])+int(config["yPad"])

    nuke.addFormat("%i %i %s" % (x, y, formatName))
    root.knob("format").setValue(formatName)

def getReadPath():
    n = nuke.thisParent()

    spec = ueSpec.Spec(n.knob("proj").value(),
                       n.knob("grp").value(),
                       n.knob("asst").value(),
                       n.knob("elclass").value(),
                       n.knob("eltype").value(),
                       n.knob("elname").value(),
                       n.knob("vers").value())

    p = "/tmp"

    if not spec.proj == "" and not spec.grp == "" and \
       not spec.asst == "" and not spec.elclass == "" and \
       not spec.eltype == "" and not spec.elname == "" and \
       not spec.vers == "":
        e = ueAssetUtils.getVersionPath(spec)
        if not e == None:
            f = ueAssetUtils.getElementName(spec)
            ext = glob.glob(os.path.join(e, "*"))[0].split(".")
            if len(ext) > 0:
                p = os.path.join(e, f+".%04d."+ext[-1])

                seq = glob.glob(os.path.join(e, f+"*"))

                nuke.thisNode().knob("first").setValue(1)
                nuke.thisNode().knob("last").setValue(len(seq))
                nuke.thisNode().knob("origfirst").setValue(1)
                nuke.thisNode().knob("origlast").setValue(len(seq))

    return p

def render():
    n = nuke.thisParent()

    spec = ueSpec.Spec(n.knob("proj").value(),
                       n.knob("grp").value(),
                       n.knob("asst").value(),
                       n.knob("elclass").value(),
                       n.knob("eltype").value(),
                       n.knob("elname").value())

    d = ueAssetUtils.getElement(spec)
    if d == None:
        d = ueCreate.createElement(spec)

    p = ueCreate.createVersion(spec, source=nuke.root().knob("name").value())

    spec.name = p["name"]

    cName = ueAssetUtils.getElementName(spec)
    cPath = os.path.join(p["path"], cName+".%04d.exr")

    nuke.thisNode().knob("file").setValue(cPath)

    ueNukeSave.ueSaveVers(comment="Auto-save of %s render." % (spec))
    nuke.tprint("Rendering '%s'" % cPath)

