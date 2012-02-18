#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

group = {}

def createGroup():
    if "name" not in group:
        print "ERROR: Group name not set"
        sys.exit(2)

    if "spec" not in group:
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(group["spec"], group["name"])

    ueCreate.createGroup(spec, group["type"], dbMeta=group["dbMeta"])

def parse():
    sArgs = "hn:s:t:d:"
    lArgs = ["help", "name=", "spec=", "type=", "directory="
             "startFrame=", "endFrame=", "frameRate=",
             "xRes=", "yRes=", "xPad=", "yPad=", "aspectRatio="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    group["spec"] = os.getenv("PROJ")
    group["type"] = "default"
    group["dbMeta"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            group["name"] = a
        elif o in ("-s", "--spec"):
            group["spec"] = a
        elif o in ("-t", "--type"):
            group["type"] = a
        elif o in ("-d", "--directory"):
            group["dbMeta"]["path"] = a
        elif o in ("--startFrame"):
            group["dbMeta"]["startFrame"] = a
        elif o in ("--endFrame"):
            group["dbMeta"]["endFrame"] = a
        elif o in ("--frameRate"):
            group["dbMeta"]["frameRate"] = a
        elif o in ("--xRes"):
            group["dbMeta"]["xRes"] = a
        elif o in ("--yRes"):
            group["dbMeta"]["yRes"] = a
        elif o in ("--xPad"):
            group["dbMeta"]["xPad"] = a
        elif o in ("--yPad"):
            group["dbMeta"]["yPad"] = a
        elif o in ("--aspectRatio"):
            group["dbMeta"]["aspectRatio"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue group."
    print ""
    print "\t-n, --name          Group name"
    print "\t-s, --spec          Destination spec"
    print "\t                    Requires at least a project"
    print "\t-t, --type          Group type"
    print "\t-d, --directory     Group directory"
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
    createGroup()

    sys.exit(0)

