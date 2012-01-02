#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings

global settings

def listGroups():
    projGroups = os.path.join(os.getenv("PROJ_ROOT"), "etc", "groups")

    groups = {}
    if os.path.exists(projGroups):
        f = open(projGroups, 'r')
        groups = json.loads(f.read())
        f.close()

    for g in groups:
        if "paths" in settings:
            print "%s -> %s" % (g, groups[g]["path"])
        else:
            print "%s" % g


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
    print "Lists groups in a ue project."
    print ""
    print "\t-p, --paths         Show the groups root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if not "PROJ" in os.environ:
        print "ERROR: No project set"
        sys.exit(2)

    settings = {}
    parse()
    listGroups()

    sys.exit(0)

