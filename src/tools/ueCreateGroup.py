#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings as ueSettings
import ueCore.AssetUtils as ueAssetUtils
import ueCore.ConfigUtils as ueConfigUtils
import ueCore.FileUtils as ueFileUtils

global group

def createGroup():
    if "name" not in group:
        print "ERROR: Group name not set"
        sys.exit(2)

    if "directory" not in group:
        print "ERROR: Directory not set"
        sysexit(2)

    config = ueConfigUtils.getConfig(os.getenv("PROJ"))
    groups = ueAssetUtils.getGroups(os.getenv("PROJ"))

    if group["name"] in groups:
        print "ERROR: Group '%s' already exists" % group["name"]
        sys.exit(2)

    if not group["type"] in config["GROUP_DIRS"]:
        print "ERROR: Group type '%s' does not exist" % group["type"]
        sys.exit(2)

    rootDir = os.path.join(group["directory"], config["GROUP_DIRS"][group["type"]][1])

    d = os.path.join(rootDir, group["name"])

    ueFileUtils.createDirTree(d, config["GROUP_DIRS"][group["type"]][0])

    groups[group["name"]] = {"path": d, "type": group["type"]}
    p = os.path.join(os.getenv("PROJ_ROOT"), "etc", "groups")
    try:
        print "Adding group to project group list '%s'" % p
        f = open(p, 'w')
        f.write(json.dumps(groups, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Adding group to project group list '%s' (%s)" % (p, e)


def parse():
    sArgs = "hn:t:d:"
    lArgs = ["help", "name=", "type=", "directory="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    group["type"] = "default"
    group["directory"] = os.getenv("PROJ_ROOT")

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            group["name"] = a
        elif o in ("-t", "--type"):
            group["type"] = a
        elif o in ("-d", "--directory"):
            group["directory"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s -n [NAME] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue group."
    print ""
    print "\t-n, --name          Group name"
    print "\t-t, --type          Group type"
    print "\t-d, --directory     Group directory"
    print "\t                    Will use project default if not set"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    if not "PROJ" in os.environ:
        print "ERROR: No project set"
        sys.exit(2)

    group = {}
    parse()
    createGroup()

    sys.exit(0)

