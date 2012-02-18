#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

settings = {}

def listAssets():
    for a in sorted(ueAssetUtils.getAssets(settings["spec"])):
        asset = a["name"]
        if "paths" in settings:
            asset = "%s -> %s" % (asset, a["path"])
        print asset

def parse():
    sArgs = "hs:p"
    lArgs = ["help", "spec=", "paths"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    settings["spec"] = ueSpec.Spec(os.getenv("PROJ"), os.getenv("GRP"))

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--spec"):
            settings["spec"] = ueSpec.Spec(a)
        elif o in ("-p", "--paths"):
            settings["paths"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s" % os.path.basename(sys.argv[0])
    print "Lists assets in a ue group."
    print ""
    print "\t-s, --spec          "
    print "\t-p, --paths         Show the groups root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    parse()
    ueClient.Client()
    listAssets()

    sys.exit(0)

