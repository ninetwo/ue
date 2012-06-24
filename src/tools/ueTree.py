#!/usr/bin/python

import sys, os, getopt, re

import ueClient, ueSpec

import ueCore
import ueCore.AssetUtils as ueAssetUtils

info = {}
info["spec"] = os.getenv("PROJ")
info["time"] = False
info["path"] = False
info["date"] = False
info["user"] = False

def printTree():
    if "spec" not in info:
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(info["spec"])

    print "Asset tree on asset:"
    print spec
    print "|"

    groups = ueAssetUtils.getGroupsList(spec)
    lastGroup = "|"
    for g, group in enumerate(sorted(groups)):
        spec.grp = group
        group = ueAssetUtils.getGroup(spec)
        if g == len(groups)-1:
            lastGroup = " "
        groupSpaceCount = 34
        printLine = "+-+-> %s" % group["name"]
        printLine += (groupSpaceCount-len(printLine))*" "
        if info["time"]:
            printLine += "%s - %s" % (str(group["startFrame"]), str(group["endFrame"]))
            groupSpaceCount += 10
            printLine += (groupSpaceCount-len(printLine))*" "
        if info["path"]:
            printLine += group["path"]
            groupSpaceCount += 30
            printLine += (groupSpaceCount-len(printLine))*" "
        if info["date"]:
            printLine += "%s, %s" % (ueCore.formatDatetime(group["created_at"]),
                                     ueCore.formatDatetime(group["updated_at"]))
            groupSpaceCount += 38
            printLine += (groupSpaceCount-len(printLine))*" "
        if info["user"]:
            printLine += group["created_by"]
        print printLine
        assets = ueAssetUtils.getAssetsList(spec)
        for asset in sorted(assets):
            spec.asst = asset
            asset = ueAssetUtils.getAsset(spec)
            assetSpaceCount = 34
            printLine = "%s +---> %s" % (lastGroup, asset["name"])
            printLine += (assetSpaceCount-len(printLine))*" "
            if info["time"]:
                printLine += "%s - %s" % (str(asset["startFrame"]), str(asset["endFrame"]))
                assetSpaceCount += 10
                printLine += (assetSpaceCount-len(printLine))*" "
            if info["path"]:
                printLine += group["path"]
                assetSpaceCount += 30
                printLine += (assetSpaceCount-len(printLine))*" "
            if info["date"]:
                printLine += "%s, %s" % (ueCore.formatDatetime(asset["created_at"]),
                                         ueCore.formatDatetime(asset["updated_at"]))
                assetSpaceCount += 38
                printLine += (assetSpaceCount-len(printLine))*" "
            if info["user"]:
                printLine += asset["created_by"]
            print printLine

    print ""

def parse():
    sArgs = "hs:tpdu"
    lArgs = ["help", "spec=", "time", "path", "date", "user"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--spec"):
            info["spec"] = a
        elif o in ("-t", "--time"):
            info["time"] = True
        elif o in ("-p", "--path"):
            info["path"] = True
        elif o in ("-d", "--date"):
            info["date"] = True
        elif o in ("-u", "--user"):
            info["user"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Provides a tree showing the ue asset heigherarchy."
    print ""
    print "\t-s, --spec          Spec"
    print "\t-t, --time          Print time information"
    print "\t-p, --path          Print the asset path"
    print "\t-d, --date          Print the creation and update times"
    print "\t-u, --user          Print the user that created the asset"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    parse()
    ueClient.Client()
    printTree()

    sys.exit(0)

