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

    maya.cmds.playbackOptions(animationStartTime=float(config["startFrame"]),
                              animationEndTime=float(config["endFrame"]),
#                              framesPerSecond=float(config["frameRate"]),
                              minTime=float(config["startFrame"]),
                              maxTime=float(config["endFrame"]))

