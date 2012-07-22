import sys

import maya.OpenMaya
import maya.OpenMayaMPx

nodeName = "ueRender"
nodeId = maya.OpenMaya.MTypeId(0x00333)

class ueRender(maya.OpenMayaMPx.MPxLocatorNode):
    test = maya.OpenMaya.MObject()

    def __init__(self):
        super(ueRender, self).__init__()


def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(ueRender())

def nodeInitializer():
    foo = maya.OpenMaya.MFnNumericAttribute()

    ueRender.test = foo.create("test", "tn", maya.OpenMaya.MFnNumericData.kBoolean, True)
    foo.setStorable(True)

    ueRender.addAttribute(ueRender.test)

def initializePlugin(mobject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject, "ue", "1.0", "Any")
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: '%s'" % nodeName)
        raise

def uninitializePlugin(mpbject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeName)
    except:
        sys.stderr.write("Failed to deregister node: '%s'" % nodeName)
        raise

