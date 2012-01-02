import os, sys, glob, re

import nuke

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

import ueNuke.Utilities as ueNukeUtils

# Get the files
files = glob.glob(os.path.join(os.getenv("PROJ_ROOT"), "tmp", "*_*_*.*"))

# Organise the files into a dict
filesDict = {}
for f in files:
    c = re.split("[_.]", os.path.basename(f))

    if c[0] not in filesDict:
        filesDict[c[0]] = {}

    if c[1] not in filesDict[c[0]]:
        filesDict[c[0]][c[1]] = {}

    if "path" not in filesDict[c[0]][c[1]]:
        filesDict[c[0]][c[1]]["path"] = os.path.join(os.path.dirname(f),
                                        "%s_%s_#####.%s" %(c[0], c[1], c[3]))
        filesDict[c[0]][c[1]]["count"] = 0

    filesDict[c[0]][c[1]]["count"] += 1

# Get asset info
proj = os.getenv("PROJ")
grp = os.getenv("GROUP")
asst = os.getenv("ASST")

# Set up our script
nuke.root().addKnob(nuke.String_Knob("proj", "project", asst))
nuke.root().addKnob(nuke.String_Knob("grp", "group", grp))
nuke.root().addKnob(nuke.String_Knob("asst", "asset", proj))
nuke.root().addKnob(nuke.String_Knob("asst_root", "asset root",
                                     os.getenv("ASST_ROOT")))

# For each layer
for t in filesDict:
    # For each pass
    for n in filesDict[t]:
        elclass = "cel"
        eltype = t
        name = n

        x = 3510
        y = 2550
        finx = 2048
        finy = 1488

        nuke.root().knob("first_frame").setValue(float(1))
        nuke.root().knob("last_frame").setValue(float(filesDict[t][n]["count"]))

        # Create nodes
        read = nuke.nodes.Read(file=filesDict[t][n]["path"],
                               first=1, last=filesDict[t][n]["count"])
        retime = nuke.nodes.Retime()
        retime.knob("input.first_lock").setValue(True)
        retime.knob("input.last_lock").setValue(True)
        retime.knob("output.first_lock").setValue(True)
        retime.knob("input.last_lock").setValue(True)
        retime.knob("input.first").setValue(0)
        retime.knob("input.last").setValue(filesDict[t][n]["count"]-1)
        retime.knob("output.first").setValue(1)
        retime.knob("output.last").setValue(filesDict[t][n]["count"])
        translate = nuke.nodes.Transform(rotate=90)
        translate.knob("center").setValue((y/2, x/2))
        reformat1 = nuke.nodes.Reformat(format="%s %s" % (x, y),
                                        resize="none")
        reformat2 = nuke.nodes.Reformat(format="%s %s" % (finx, finy),
                                        resize="width",
                                        filter="Cubic")
        write = nuke.nodes.Write(name="write"+t+n)

        # Join nodes
        retime.setInput(0, read)
        translate.setInput(0, retime)
        reformat1.setInput(0, translate)
        reformat2.setInput(0, reformat1)
        write.setInput(0, reformat2)

        # Get/create the element
        d = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
        if d == None:
            d = ueCreateUtils.createElement(proj, grp, asst,
                                            elclass, eltype, name)

        # Get the new version and file name
        vers = ueAssetUtils.getVersions(proj, grp, asst,
                                        elclass, eltype, name)
        cName = ueCreateUtils.getElementName(proj, grp, asst,
                                             elclass, eltype, name,
                                             len(vers)+1)

        # Create new version
        p = ueCreateUtils.createVersion(proj, grp, asst,
                                        elclass, eltype, name,
                                        len(vers)+1,
                                        source=filesDict[t][n]["path"])
        cPath = os.path.join(p["path"], cName+".%04d.exr")

        # Set up the write
        write.knob("file").setValue(cPath)
        write.knob("file_type").setValue("exr")
        write.knob("channels").setValue("rgba")

        # Render
        nuke.execute("write"+t+n, 1, filesDict[t][n]["count"], 1)

# Save the script
ueNukeUtils.saveUtility(proj, grp, asst, "c", "cel", "master")

