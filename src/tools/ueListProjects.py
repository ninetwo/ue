#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings

global settings

def listProjects():
    projects = {}
    if os.path.exists(ueCore.Settings.__UE_PROJ_FILE_PATH__):
        f = open(ueCore.Settings.__UE_PROJ_FILE_PATH__, 'r')
        projects = json.loads(f.read())
        f.close()

    for p in sorted(projects):
        if "paths" in settings:
            print "%s -> %s" % (p, projects[p]["path"])
        else:
            print "%s" % p


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
    settings = {}
    parse()
    listProjects()

    sys.exit(0)

