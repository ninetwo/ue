#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings

global settings

def listAssets():
    if "group" not in settings:
        print "ERROR: Group not set"
        sys.exit(2)

    projGroups = os.path.join(os.getenv("PROJ_ROOT"), "etc", "groups")

    groups = {}
    if os.path.exists(projGroups):
        f = open(projGroups, 'r')
        groups = json.loads(f.read())
        f.close()

    if settings["group"] not in groups:
        print "ERROR: Group '%s' not found" % settings["group"]
        sys.exit(2)

    groupAssets = os.path.join(groups[settings["group"]]["path"], "etc", "assets")

    assets = {}
    if os.path.exists(groupAssets):
        f = open(groupAssets, 'r')
        assets = json.loads(f.read())
        f.close()

    for a in sorted(assets):
        if "paths" in settings:
            print "%s -> %s" % (a, assets[a]["path"])
        else:
            print "%s" % a


def parse():
    sArgs = "hg:p"
    lArgs = ["help", "group=", "paths"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    if "GROUP" in os.environ:
        settings["group"] = os.getenv("GROUP")

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-g", "--group"):
            settings["group"] = a
        elif o in ("-p", "--paths"):
            settings["paths"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s" % os.path.basename(sys.argv[0])
    print "Lists assets in a ue group."
    print ""
    print "\t-g, --group         Group to list"
    print "\t-p, --paths         Show the groups root paths"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if not "PROJ" in os.environ:
        print "ERROR: No project set"
        sys.exit(2)

    settings = {}
    parse()
    listAssets()

    sys.exit(0)

