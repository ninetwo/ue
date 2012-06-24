#!/usr/bin/python

import sys, os, getopt, re

import ueClient, ueSpec

import ueCore
import ueCore.AssetUtils as ueAssetUtils

info = {}

def printInfo():
    if "spec" not in info:
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(info["spec"])

    if spec.grp == None:
        # Project info
        assetType = "project"
        assetInfo = ueAssetUtils.getProject(spec)
    elif spec.asst == None:
        # Group info
        assetType = "group"
        assetInfo = ueAssetUtils.getGroup(spec)
    elif spec.elclass == None and \
         spec.eltype == None and \
         spec.elname == None:
        # Asset info
        assetType = "asset"
        assetInfo = ueAssetUtils.getAsset(spec)
    elif spec.vers == None:
        # Element info
        assetType = "element"
        assetInfo = ueAssetUtils.getElement(spec)
        assetInfo = assetInfo[spec.elclass][spec.eltype][spec.elname]
    elif spec.elpass == None:
        # Version info
        assetType = "version"
        assetInfo = ueAssetUtils.getVersions(spec)[int(spec.vers)-1]
    else:
        print "ERROR: Could not identify spec as a valid element"
        sys.exit(2)

    print "Information on %s:\n%s\n" % (assetType, str(info["spec"]))

    for a in sorted(assetInfo):
        # Get a padding value so the key/value columns will be neatly aligned
        spacePadding = 28-len(a)

        # Parse the version and datetime info correctly
        if a == "versions":
            assetInfo[a] = len(assetInfo[a])
        elif a in ["created_at", "updated_at"]:
            assetInfo[a] = ueCore.formatDatetime(str(assetInfo[a]))

        # Get rid of the keys with _id because they're database stuff
        if not re.match(".*_id$", a):
            print "%s:%s%s" % (a, " "*spacePadding, str(assetInfo[a]))

    print ""

def parse():
    sArgs = "hs:"
    lArgs = ["help", "spec="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    info["spec"] = "%s:%s:%s" % (os.getenv("PROJ"),
                                 os.getenv("GRP"),
                                 os.getenv("ASST"))

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--spec"):
            info["spec"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Provides information on any ue project,"
    print "group, asset, element or version."
    print ""
    print "\t-s, --spec          Spec"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    parse()
    ueClient.Client()
    printInfo()

    sys.exit(0)

