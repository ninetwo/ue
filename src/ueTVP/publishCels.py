import os, sys, glob, re

import ueSpec

import ueNuke.Utilities as ueNukeUtils
import ueNuke.Render as ueNukeRender

import nuke

# File path and file name
# File names will be: animationLayer_colourLayer.frameNumber.extension
path = os.path.join(os.getenv("ASST_ROOT"), "tmp/fromTVP")
name = "*_*.*.*"

if not os.path.exists(path):
    print "ERROR: No files found"
    sys.exit(2)

# Get the files
files = glob.glob(os.path.join(path, name))

# Organise them into a dict
filesDict = {}
for f in files:
    c = os.path.basename(f).split(".")
    d = c[0].split("_")

    animationLayer = d[0]
    colourLayer = d[1]
    extension = c[2]

    if animationLayer not in filesDict:
        filesDict[animationLayer] = {}

    if colourLayer not in filesDict[animationLayer]:
        filesDict[animationLayer][colourLayer] = {}

    if "path" not in filesDict[animationLayer][colourLayer]:
        filesDict[animationLayer][colourLayer]["path"] = os.path.join(os.path.dirname(f),
                                                         animationLayer+"_"+colourLayer+".%04d."+extension)
        filesDict[animationLayer][colourLayer]["count"] = 0

    filesDict[animationLayer][colourLayer]["count"] += 1

# Get context and spec
context = ueSpec.Context()
spec = context.spec
spec.elclass = "ns"
spec.eltype = "cel"
spec.elname = "master"

# Save the names of our write nodes
writeNodes = []

# For each layer
for t in filesDict:
    # For each pass
    for n in filesDict[t]:
        elclass = "cel"
        eltype = t
        elname = n

        x = 3510
        y = 2550
        finx = 2048
        finy = 1488

        # Override the shot frame ranges
        nuke.root().knob("first_frame").setValue(float(1))
        nuke.root().knob("last_frame").setValue(float(filesDict[t][n]["count"]))

        # Create nodes
        # The retime is incase we're given a 0 frame
        read = nuke.nodes.Read(file=filesDict[t][n]["path"],
                               first=1, last=filesDict[t][n]["count"])
        retime = nuke.nodes.Retime()
        retime.knob("input.first_lock").setValue(True)
        retime.knob("input.last_lock").setValue(True)
        retime.knob("output.first_lock").setValue(True)
        retime.knob("output.last_lock").setValue(True)
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
        write = ueWriteAsset("Write", name="write%s%s" % (eltype, elname))

        # Join nodes
        retime.setInput(0, read)
        translate.setInput(0, retime)
        reformat1.setInput(0, translate)
        reformat2.setInput(0, reformat1)
        write.setInput(0, reformat2)

        # Set up the write nodes write asset
        write.knob("proj").setValue(spec.proj)
        write.knob("grp").setValue(spec.grp)
        write.knob("asst").setValue(spec.asst)
        write.knob("elclass").setValue(elclass)
        write.knob("eltype").setValue(eltype)
        write.knob("elname").setValue(elname)

        # Set up the write node compression
        # To save disk space, only write out the full rgba for line layers
        # The stuff coming out of TVP is greyscale anyway, so the colour channels
        # should be identical anyway
        write.knob("file_type").setValue("exr")
        write.knob("datatype").setValue("16 bit half")
        write.knob("compression").setValue("PIZ Wavelet (32 scanlines")
        if re.match(".*Line$", elname, flags=re.IGNORECASE):
            write.knob("channels").setValue("rgba")
        else:
            write.knob("channels").setValue("r")

        writeNodes.append(write.name())

# Save the script
ueNukeUtils.saveUtility(spec)

print writeNodes

# Render
#ueNukeRender.runRender([0, writeNodes, {"newVersion": True, "clearLastVersion": False}])

