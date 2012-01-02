import os, sys

import nuke

import ueCore.AssetUtils as ueAssetUtils

def createProjectsKnob():
    node = nuke.thisNode()
    projKnob = nuke.Enumeration_Knob("proj", "project",
                                     ueAssetUtils.getProjectsList())
    node.addKnob(projKnob)
    projKnob.setValue(os.getenv("PROJ"))

def createGroupsKnob():
    node = nuke.thisNode()
    grpKnob = nuke.Enumeration_Knob("grp", "group",
                                    ueAssetUtils.getGroupsList(node.knob("proj").value()))
    node.addKnob(grpKnob)
    grpKnob.setValue(os.getenv("GROUP"))

def createAssetsKnob():
    node = nuke.thisNode()
    asstKnob = nuke.Enumeration_Knob("asst", "asset",
                                     ueAssetUtils.getAssetsList(node.knob("proj").value(), node.knob("grp").value()))
    node.addKnob(asstKnob)
    asstKnob.setValue(os.getenv("ASST"))

def createClassesKnob():
    node = nuke.thisNode()
    classKnob = nuke.Enumeration_Knob("elclass", "class",
                                      ueAssetUtils.getClassesList(node.knob("proj").value(), node.knob("grp").value(), node.knob("asst").value()))
    node.addKnob(classKnob)

def createTypesKnob():
    node = nuke.thisNode()
    typesKnob = nuke.Enumeration_Knob("eltype", "type",
                                      ueAssetUtils.getTypesList(node.knob("proj").value(), node.knob("grp").value(), node.knob("asst").value(), node.knob("elclass").value()))
    node.addKnob(typesKnob)

def createNamesKnob():
    node = nuke.thisNode()
    namesKnob = nuke.Enumeration_Knob("elname", "name",
                                      ueAssetUtils.getNamesList(node.knob("proj").value(), node.knob("grp").value(), node.knob("asst").value(), node.knob("elclass").value(), node.knob("eltype").value()))
    node.addKnob(namesKnob)

def createElementsKnob():
    createProjectsKnob()
    createGroupsKnob()
    createAssetsKnob()
    createClassesKnob()
    createTypesKnob()
    createNamesKnob()

def initElementsKnob():
    n = nuke.thisNode()
    if not n.knob("projmenu") == None:
        n.knob("projmenu").setValues(ueAssetUtils.getProjectsList())
        n.knob("projmenu").setFlag(nuke.DO_NOT_WRITE)
#        n.knob("projmenu").setValue(nuke.knob("PROJ"))
    if not n.knob("grpmenu") == None:
        n.knob("grpmenu").setValues(ueAssetUtils.getGroupsList(
                                    n.knob("projmenu").value()))
        n.knob("grpmenu").setFlag(nuke.DO_NOT_WRITE)
#        n.knob("grpmenu").setValue(os.getenv("GROUP"))
    if not n.knob("asstmenu") == None:
        n.knob("asstmenu").setValues(ueAssetUtils.getAssetsList(
                                     n.knob("projmenu").value(),
                                     n.knob("grpmenu").value()))
        n.knob("asstmenu").setFlag(nuke.DO_NOT_WRITE)
#        n.knob("asstmenu").setValue(os.getenv("ASST"))
#    if not n.knob("elclassmenu") == None:
#        n.knob("elclassmenu").setValues(ueAssetUtils.getClassesList(
#                                        n.knob("projmenu").value(),
#                                        n.knob("grpmenu").value(),
#                                        n.knob("asstmenu").value()))
    if not n.knob("eltypemenu") == None:
        n.knob("eltypemenu").setValues(ueAssetUtils.getTypesList(
                                       n.knob("projmenu").value(),
                                       n.knob("grpmenu").value(),
                                       n.knob("asstmenu").value(),
                                       n.knob("elclassmenu").value()))
        n.knob("eltypemenu").setFlag(nuke.DO_NOT_WRITE)
#        n.knob("eltypebox").setFlag(nuke.DO_NOT_WRITE)
    if not n.knob("elnamemenu") == None:
        n.knob("elnamemenu").setValues(ueAssetUtils.getNamesList(
                                       n.knob("projmenu").value(),
                                       n.knob("grpmenu").value(),
                                       n.knob("asstmenu").value(),
                                       n.knob("elclassmenu").value(),
                                       n.knob("eltypemenu").value()))
        n.knob("elnamemenu").setFlag(nuke.DO_NOT_WRITE)
#        n.knob("elnamebox").setFlag(nuke.DO_NOT_WRITE)
    if not n.knob("versmenu") == None:
        t = ueAssetUtils.getVersions(
                                     n.knob("projmenu").value(),
                                     n.knob("grpmenu").value(),
                                     n.knob("asstmenu").value(),
                                     n.knob("elclassmenu").value(),
                                     n.knob("eltypemenu").value(),
                                     n.knob("elnamemenu").value())
        v = []
        for i in range(1, len(t)+1):
            v.append(i)
        n.knob("versmenu").setValues(v)
        n.knob("versmenu").setFlag(nuke.DO_NOT_WRITE)

def updateElementsKnob():
    node = nuke.thisNode()
    t = ["test"]
    if nuke.thisKnob().name() == "projmenu":
        t = ueAssetUtils.getGroupsList(node.knob("projmenu").value())
        node.knob("grpmenu").setValues(t)
    if nuke.thisKnob().name() in ("projmenu", "grpmenu") and not t == []:
        t = ueAssetUtils.getAssetsList(node.knob("projmenu").value(),
                                       node.knob("grpmenu").value())
        node.knob("asstmenu").setValues(t)
    #if nuke.thisKnob().name() in ("projmenu", "grpmenu", "asstmenu") and not t == []:
#        t = ueAssetUtils.getClassesList(node.knob("projmenu").value(),
#                                        node.knob("grpmenu").value(),
#                                        node.knob("asstmenu").value())
#        node.knob("elclassmenu").setValues(t)
        #node.knob("asst").setValue(node.knob("asstmenu").value())
    if nuke.thisKnob().name() in ("projmenu", "grpmenu", "asstmenu", "elclassmenu") and not t == []:
        t = ueAssetUtils.getTypesList(node.knob("projmenu").value(),
                                      node.knob("grpmenu").value(),
                                      node.knob("asstmenu").value(),
                                      node.knob("elclassmenu").value())
        node.knob("eltypemenu").setValues(t)
    if nuke.thisKnob().name() in ("projmenu", "grpmenu", "asstmenu", "elclassmenu", "eltypemenu") and not t == []:
        t = ueAssetUtils.getNamesList(node.knob("projmenu").value(),
                                      node.knob("grpmenu").value(),
                                      node.knob("asstmenu").value(),
                                      node.knob("elclassmenu").value(),
                                      node.knob("eltypemenu").value())
        node.knob("elnamemenu").setValues(t)
    if nuke.thisKnob().name() in ("projmenu", "grpmenu", "asstmenu", "elclassmenu", "eltypemenu", "versmenu") and not t == []:
        t = ueAssetUtils.getVersions(node.knob("projmenu").value(),
                                      node.knob("grpmenu").value(),
                                      node.knob("asstmenu").value(),
                                      node.knob("elclassmenu").value(),
                                     node.knob("eltypemenu").value(),
                                     node.knob("elnamemenu").value())
        v = []
        for i in range(1, len(t)+1):
            v.append(i)
        if not node.knob("versmenu") == None:
            node.knob("versmenu").setValues(v)


