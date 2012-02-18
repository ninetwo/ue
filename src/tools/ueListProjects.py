#!/usr/bin/python

import sys, os, getopt

import ueClient

import ueCore.AssetUtils as ueAssetUtils

settings = {}

def listProjects():
    for p in sorted(ueAssetUtils.getProjects()):
        project = p["name"]
        if "paths" in settings:
            project = "%s -> %s" % (project, p["path"])
        print project

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
    print "Lists ue projects."
    print ""
    print "\t-p, --paths         Show the project root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    parse()
    ueClient.Client()
    listProjects()

    sys.exit(0)

