#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Destroy as ueDestroy

global group
group = ""

def destroyGroup():
    if group == "":
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(group)

    ueDestroy.destroyGroup(spec)

def parse():
    global group

    sArgs = "hs:"
    lArgs = ["help", "spec="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    group = os.getenv("PROJ")

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--spec"):
            group = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Deletes a ue group."
    print ""
    print "\t-s, --spec          Group spec"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    ueClient.Client()
    destroyGroup()

    sys.exit(0)

