import os, sys
import re, glob

import nuke, nukescripts

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

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

#
# Adds custom knobs to save asset info
# Sets up scene from asset info
#
def ueNewScriptSetup():
    root = nuke.root()

    formatName = "ueProjectRes"

    root.addKnob(nuke.String_Knob("proj", "project",
                                  os.getenv("PROJ")))
    root.addKnob(nuke.String_Knob("grp", "group",
                                  os.getenv("GROUP")))
    root.addKnob(nuke.String_Knob("asst", "asset",
                                  os.getenv("ASST")))
    root.addKnob(nuke.String_Knob("asst_root", "asset root",
                                  os.getenv("ASST_ROOT")))

    root.knob("fps").setValue(int(os.getenv("FRAMERATE")))
    root.knob("first_frame").setValue(int(os.getenv("STARTFRAME")))
    root.knob("last_frame").setValue(int(os.getenv("ENDFRAME")))

    x = int(os.getenv("XRES"))+int(os.getenv("XPAD"))
    y = int(os.getenv("YRES"))+int(os.getenv("YPAD"))

    nuke.addFormat("%i %i %s" % (x, y, formatName))
    root.knob("format").setValue(formatName)

def getReadPath():
    n = nuke.thisParent()

    proj = n.knob("proj").value()
    grp = n.knob("grp").value()
    asst = n.knob("asst").value()
    elclass = n.knob("elclass").value()
    eltype = n.knob("eltype").value()
    name = n.knob("elname").value()
    vers = n.knob("vers").value()

    p = "/tmp"

    if not proj == "" and not grp == "" and not asst == "" and \
       not elclass == "" and not eltype == "" and not name == "" and \
       not vers == "":
        e = ueCreateUtils.getVersionPath(proj, grp, asst, elclass,
                                         eltype, name, int(vers))
        if not e == None:
            f = ueCreateUtils.getElementName(proj, grp, asst,
                                             elclass, eltype, name, int(vers))
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

    proj = n.knob("proj").value()
    grp = n.knob("grp").value()
    asst = n.knob("asst").value()
    elclass = n.knob("elclass").value()
    eltype = n.knob("eltype").value()
    name = n.knob("elname").value()

    d = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    if d == None:
        d = ueCreateUtils.createElement(proj, grp, asst, elclass, eltype, name)

    vers = ueAssetUtils.getVersions(proj, grp, asst, elclass, eltype, name)
    cName = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, len(vers)+1)

    p = ueCreateUtils.createVersion(proj, grp, asst, elclass, eltype, name, len(vers)+1,
                                    source=nuke.root().knob("name").value())
    cPath = os.path.join(p["path"], cName+".%04d.exr")

    nuke.thisNode().knob("file").setValue(cPath)

    ueNukeSave.ueSaveVers()
    nuke.tprint("Rendering '%s'" % cPath)

#
# Checks the current script against asset info
#
def ueScriptSanityCheck():
    root = nuke.root()

    if not root.knob("fps").value() == int(os.getenv("FRAMERATE")):
        if nuke.ask("Frame rate does not match asset frame rate.\n\n"+\
                        "Update to current frame rate or not?"):
            root.knob("fps").setValue(int(os.getenv("FRAMERATE")))

    if not root.knob("first_frame").value() == int(os.getenv("STARTFRAME")):
        if nuke.ask("Start frame does not match asset start frame.\n\n"+\
                        "Update to current start frame or not?"):
            root.knob("first_frame").setValue(int(os.getenv("STARTFRAME")))

    if not root.knob("last_frame").value() == int(os.getenv("ENDFRAME")):
        if nuke.ask("End frame does not match asset end frame.\n\n"+\
                        "Update to current end frame or not?"):
            root.knob("last_frame").setValue(int(os.getenv("ENDFRAME")))

    if root.knob("proj") == None or root.knob("grp") == None or\
       root.knob("asst") == None or root.knob("asst_root") == None:
        root.addKnob(nuke.String_Knob("proj", "project", os.getenv("PROJ")))
        root.addKnob(nuke.String_Knob("grp", "group", os.getenv("GROUP")))
        root.addKnob(nuke.String_Knob("asst", "asset", os.getenv("ASST")))
        root.addKnob(nuke.String_Knob("asst_root", "asset root", os.getenv("ASST_ROOT")))

    if not root.knob("proj").value() == os.getenv("PROJ"):
        if nuke.ask("Script project does not match current project.\n\n"+\
                    "Update to current project?"):
            root.knob("proj").setValue(os.getenv("PROJ"))
        else:
            return False

    if not root.knob("grp").value() == os.getenv("GROUP"):
        if nuke.ask("Script group does not match current group.\n\n"+\
                    "Update to current group?"):
            root.knob("grp").setValue(os.getenv("GROUP"))
        else:
            return False

    if not root.knob("asst").value() == os.getenv("ASST"):
        if nuke.ask("Script asset does not match current asset.\n\n"+\
                    "Update to current asset?"):
            root.knob("asst").setValue(os.getenv("ASST"))
        else:
            return False

    if not root.knob("asst_root").value() == os.getenv("ASST_ROOT"):
        if nuke.ask("Script asset path does not match current asset path.\n\n"+\
                    "It's likely the asset has been moved. "+\
                    "Update to current asset path?"):
            root.knob("asst_root").setValue(os.getenv("ASST_ROOT"))
        else:
            return False

    return True

