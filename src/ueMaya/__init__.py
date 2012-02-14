import os

import maya.cmds
import maya.OpenMayaUI
import sip

import ueSpec

import ueCore.Config as ueConfig

from PyQt4 import QtCore

def getMayaWindow():
    ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

# Parses the fileInfo from a list to a dict
def parseFileInfo(fi):
    fiDict = {}
    for i in range(len(fi)/2):
        fiDict[fi[i*2]] = fi[i*2+1]
    return fiDict

def ueNewScriptSetup():
    spec = ueSpec.Spec(os.getenv("PROJ"),
                       os.getenv("GRP"),
                       os.getenv("ASST"))

    config = ueConfig.Config(spec).config["assetSettings"]

    # Set up renderer - default to Mental Ray
    maya.cmds.loadPlugin("Mayatomr.so")
    maya.cmds.setAttr("defaultRenderGlobals.currentRenderer", "mentalRay", type="string")

    # Set up the timeline
    maya.cmds.playbackOptions(animationStartTime=float(config["startFrame"]),
                              animationEndTime=float(config["endFrame"]),
                              minTime=float(config["startFrame"]),
                              maxTime=float(config["endFrame"]))

    x = int(config["xRes"])+int(config["xPad"])
    y = int(config["yRes"])+int(config["yPad"])

    # Set up renderGlobals
    maya.cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
    maya.cmds.setAttr("defaultRenderGlobals.animation", 1)
    maya.cmds.setAttr("defaultRenderGlobals.startFrame", float(config["startFrame"]))
    maya.cmds.setAttr("defaultRenderGlobals.endFrame", float(config["endFrame"]))
    maya.cmds.setAttr("defaultResolution.pixelAspect", float(config["aspectRatio"]))
    maya.cmds.setAttr("defaultResolution.deviceAspectRatio", float(x)/float(y))
    maya.cmds.setAttr("defaultResolution.width", x)
    maya.cmds.setAttr("defaultResolution.height", y)

    # Render file name
    #maya.cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
    #maya.cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)

