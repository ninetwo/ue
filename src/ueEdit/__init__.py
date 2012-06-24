import os, json

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

def getEditFromSpec(spec):
    editAsset = ueAssetUtils.getVersion(spec)

    if not editAsset:
        return {}

    editFile = os.path.join(editAsset["path"], editAsset["file_name"]+".conf")

    spec.vers = editAsset["version"]

    print "Reading edit from:"
    print spec
    print ""

    f = open(editFile, "r")
    edit = json.load(f)
    f.close()

    return edit

def getEdit(spec):
    edit = getEditFromSpec(spec)

    checkedEdit = {}

    if "sequences" not in edit:
        print "ERROR: Sequences undefined"
    else:
        checkedEdit["sequences"] = []
        for sequence in edit["sequences"]:
            if sequence not in  edit:
                print "ERROR: Undefined sequence '%s'" % shot
                continue
            if "shots" not in edit[sequence]:
                print "ERROR: Shots undefined in sequence '%s'" % sequence
                continue
            if sequence not in checkedEdit:
                checkedEdit[sequence] = {}
            checkedEdit[sequence]["shots"] = []
            checkedEdit["sequences"].append(sequence)
            for shot in edit[sequence]["shots"]:
                if shot not in edit[sequence]:
                    print "ERROR: Undefined shot '%s'" % shot
                    continue
                checkedEdit[sequence][shot] = edit[sequence][shot]
                checkedEdit[sequence]["shots"].append(shot)

    return checkedEdit

def getBuild(spec):
    edit = getEditFromSpec(spec)

    if "sequences" in edit:
        del edit["sequences"]
    for sequence in edit:
        if "shots" in edit[sequence]:
            del edit[sequence]["shots"]

    return edit

