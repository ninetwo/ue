#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

project = {}

def createProject():
    if "name" not in project:
        print "ERROR: Project name not set"
        sys.exit(2)

    if "directory" not in project:
        print "ERROR: Project directory not set"
        sys.exit(2)

    spec = ueSpec.Spec(project["name"])

    ueCreate.createProject(spec)

def parse():
    sArgs = "hn:d:"
    lArgs = ["help", "name=", "directory="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    project["directory"] = "/work"

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

    ueClient.Client()

    parse()
    createProject()

    sys.exit(0)

