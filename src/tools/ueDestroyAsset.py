#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Destroy as ueDestroy

global asset
asset = ""

def destroyAsset():
    if asset == "":
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(asset)

    ueDestroy.destroyAsset(spec)

def parse():
    global asset

    sArgs = "hs:"
    lArgs = ["help", "spec="]

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
            asset = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Deletes a ue asset."
    print ""
    print "\t-s, --spec          Asset spec"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    ueClient.Client()
    destroyAsset()

    sys.exit(0)

