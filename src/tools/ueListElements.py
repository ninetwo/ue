#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

settings = {}

def listElements():
    elements = ueAssetUtils.getElements(settings["spec"])

    for e in sorted(elements):
        for t in sorted(elements[e]):
            for n in sorted(elements[e][t]):
                a = ueSpec.Spec(settings["spec"].proj,
                                settings["spec"].grp,
                                settings["spec"].asst,
                                e, t, n)
                if "paths" in settings:
                    print "%s -> %s" % (str(a), elements[e][t][n]["path"])
                else:
                    print "%s" % str(a)


def parse():
    sArgs = "hs:p"
    lArgs = ["help", "spec=", "paths"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    settings["spec"] = ueSpec.Spec(os.getenv("PROJ"),
                                   os.getenv("GRP"),
                                   os.getenv("ASST"))

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
    print "Lists elements in a ue asset."
    print ""
    print "\t-s, --spec          "
    print "\t-p, --paths         Show the element root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    ueClient.Client()

    parse()
    listElements()

    sys.exit(0)

