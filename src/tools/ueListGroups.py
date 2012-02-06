#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

settings = {}

def listGroups():
    for g in sorted(ueAssetUtils.getGroupsList(settings["spec"])):
        if "paths" in settings:
            print "%s -> %s" % (g, groups[g]["path"])
        else:
            print "%s" % g


def parse():
    sArgs = "hs:p"
    lArgs = ["help", "spec=", "paths"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    settings["spec"] = ueSpec.Spec(os.getenv("PROJ"))

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
    print "Lists groups in a ue project."
    print ""
    print "\t-s, --spec          "
    print "\t-p, --paths         Show the groups root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    ueClient.Client()

    parse()
    listGroups()

    sys.exit(0)

