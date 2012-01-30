import maya.OpenMayaUI as mui
import sip

from PyQt4 import QtCore

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

# Parses the fileInfo from a list to a dict
def parseFileInfo(fi):
    fiDict = {}
    for i in range(len(fi)/2):
        fiDict[fi[i*2]] = fi[i*2+1]
    return fiDict

