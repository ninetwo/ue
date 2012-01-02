#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.AssetUtils as ueAssetUtils

global settings

def listElements():
    proj = os.getenv("PROJ")
    grp = os.getenv("GROUP")
    asst = os.getenv("ASST")

    elements = ueAssetUtils.getElements(proj, grp, asst)

    for e in elements:
        for t in elements[e]:
            for n in elements[e][t]:
                a = ":".join([proj, grp, asst, n, t, e])
                if "paths" in settings:
                    print "%s -> %s" % (a, elements[e][t][n]["path"])
                else:
                    print "%s" % a


def parse():
    sArgs = "hp"
    lArgs = ["help", "paths"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-p", "--paths"):
            settings["paths"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s" % os.path.basename(sys.argv[0])
    print "Lists elements in a ue asset."
    print ""
    print "\t-p, --paths         Show the element root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if not "PROJ" in os.environ or \
       not "GROUP" in os.environ or \
       not "ASST" in os.environ:
        print "ERROR: No asset set"
        sys.exit(2)

    settings = {}
    parse()
    listElements()

    sys.exit(0)

