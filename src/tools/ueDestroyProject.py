#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Destroy as ueDestroy

global project
project = ""

def deleteProject():
    if project == "":
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(project)

    ueDestroy.destroyProject(spec)

def parse():
    global project

    sArgs = "hs:"
    lArgs = ["help", "spec="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--spec"):
            project = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] ..." % os.path.basename(sys.argv[0])
    print "Deletes a ue project."
    print ""
    print "\t-n, --spec          Project spec"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    ueClient.Client()
    deleteProject()

    sys.exit(0)

