#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings as ueSettings
import ueCore.AssetUtils as ueAssetUtils
import ueCore.FileUtils as ueFileUtils
import ueCore.ConfigUtils as ueConfigUtils

global project

def createProject():
    if "name" not in project:
        print "ERROR: Project name not set"
        sys.exit(2)

    if "directory" not in project:
        print "ERROR: Project directory not set"
        sys.exit(2)

    config = ueConfigUtils.getConfig()
    projects = ueAssetUtils.getProjects()

    if project["name"] in projects:
        print "ERROR: Project '%s' already exists" % project["name"]
        sys.exit(2)

    if not os.path.exists(project["directory"]):
        print "ERROR: Path '%s' not found" % project["directory"]
        sys.exit(2)

    d = os.path.join(project["directory"], project["name"])

    ueFileUtils.createDirTree(d, config["PROJECT_DIRS"])
    ueConfigUtils.saveConfig(config, d)

    projects[project["name"]] = {"path": d}
    try:
        print "Adding project to projects list '%s'" % ueSettings.__UE_PROJ_FILE_PATH__
        f = open(ueSettings.__UE_PROJ_FILE_PATH__, "w")
        f.write(json.dumps(projects, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Adding project to projects list '%s' (%s)" % (ueSettings.__UE_PROJ_FILE_PATH__, e)
        sys.exit(2)


def parse():
    sArgs = "hn:d:"
    lArgs = ["help", "name=", "directory="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    project["directory"] = ueSettings.__UE_ROOT__

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            project["name"] = a
        elif o in ("-d", "--directory"):
            project["directory"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s -n [NAME] -d [DIRECTORY]" % os.path.basename(sys.argv[0])
    print "Creates a new ue project."
    print ""
    print "\t-n, --name          Project name"
    print "\t-d, --directory     Root directory"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    project = {}
    parse()
    createProject()

    sys.exit(0)

