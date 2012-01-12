import maya.OpenMayaUI as mui
import sip

from PyQt4 import QtCore

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

