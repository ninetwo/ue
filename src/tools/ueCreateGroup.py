#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

group = {}

def createGroup():
    if "name" not in group:
        print "ERROR: Group name not set"
        sys.exit(2)

    spec = ueSpec.Spec(group["spec"], group["name"])

    ueCreate.createGroup(spec, group["type"], dbMeta=group["dbMeta"])


def parse():
    sArgs = "hn:s:t:d:"
    lArgs = ["help", "name=", "spec=", "type=", "directory="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    group["spec"] = os.getenv("PROJ")
    group["type"] = "default"
    group["dbMeta"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            group["name"] = a
        elif o in ("-s", "--spec"):
            group["spec"] = a
        elif o in ("-t", "--type"):
            group["type"] = a
        elif o in ("-d", "--directory"):
            group["dbMeta"]["path"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s -n [NAME] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue group."
    print ""
    print "\t-n, --name          Group name"
    print "\t-s, --spec          Spec to create group in"
    print "\t-t, --type          Group type"
    print "\t-d, --directory     Group directory"
    print "\t                    Will use project default if not set"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    ueClient.Client()

    parse()
    createGroup()

    sys.exit(0)

