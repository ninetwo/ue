#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

asset = {}

def createAsset():
    if "name" not in asset:
        print "ERROR: Asset name not set"
        sys.exit(2)

    if "spec" not in asset:
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec("%s:%s" % (asset["spec"], asset["name"]))

    ueCreate.createAsset(spec, asset["type"], dbMeta=asset["dbMeta"])

def parse():
    sArgs = "hn:s:t:d:"
    lArgs = ["help", "name=", "spec=", "type=", "directory=",
             "startFrame=", "endFrame=", "frameRate=",
             "xRes=", "yRes=", "xPad=", "yPad=", "aspectRatio="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    asset["spec"] = "%s:%s" % (os.getenv("PROJ"), os.getenv("GRP"))
    asset["type"] = "default"
    asset["dbMeta"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            asset["name"] = a
        elif o in ("-s", "--spec"):
            asset["spec"] = a
        elif o in ("-t", "--type"):
            asset["type"] = a
        elif o in ("-d", "--directory"):
            asset["dbMeta"]["path"] = a
        elif o in ("--startFrame"):
            asset["dbMeta"]["startFrame"] = a
        elif o in ("--endFrame"):
            asset["dbMeta"]["endFrame"] = a
        elif o in ("--frameRate"):
            asset["dbMeta"]["frameRate"] = a
        elif o in ("--xRes"):
            asset["dbMeta"]["xRes"] = a
        elif o in ("--yRes"):
            asset["dbMeta"]["yRes"] = a
        elif o in ("--xPad"):
            asset["dbMeta"]["xPad"] = a
        elif o in ("--yPad"):
            asset["dbMeta"]["yPad"] = a
        elif o in ("--aspectRatio"):
            asset["dbMeta"]["aspectRatio"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue asset."
    print ""
    print "\t-n, --name          Asset name"
    print "\t-s, --spec          Destination spec"
    print "\t                    Requires at least a project"
    print "\t                    and a group"
    print "\t-t, --type          Asset type"
    print "\t-d, --directory     Asset directory"
    print "\t--startFrame        Start frame (float)"
    print "\t--endFrame          End frame (float)"
    print "\t--frameRate         Frames per second (float)"
    print "\t--xRes              X resolution (float)"
    print "\t--yRes              Y resolution (float)"
    print "\t--xPad              Total X padding (float)"
    print "\t--yPad              Total Y padding (float)"
    print "\t--aspectRatio       Pixel aspect ratio (float)"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    ueClient.Client()
    createAsset()

    sys.exit(0)

