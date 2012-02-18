#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

project = {}

def createProject():
    if "name" not in project:
        print "ERROR: Project name not set"
        sys.exit(2)

    spec = ueSpec.Spec(project["name"])

    ueCreate.createProject(spec, dbMeta=project["dbMeta"])

def parse():
    sArgs = "hn:d:"
    lArgs = ["help", "name=", "directory=",
             "startFrame=", "endFrame=", "frameRate=",
             "xRes=", "yRes=", "xPad=", "yPad=", "aspectRatio="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    project["dbMeta"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            project["name"] = a
        elif o in ("-d", "--directory"):
            project["dbMeta"]["path"] = a
        elif o in ("--startFrame"):
            project["dbMeta"]["startFrame"] = a
        elif o in ("--endFrame"):
            project["dbMeta"]["endFrame"] = a
        elif o in ("--frameRate"):
            project["dbMeta"]["frameRate"] = a
        elif o in ("--xRes"):
            project["dbMeta"]["xRes"] = a
        elif o in ("--yRes"):
            project["dbMeta"]["yRes"] = a
        elif o in ("--xPad"):
            project["dbMeta"]["xPad"] = a
        elif o in ("--yPad"):
            project["dbMeta"]["yPad"] = a
        elif o in ("--aspectRatio"):
            project["dbMeta"]["aspectRatio"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -n [NAME] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue project."
    print ""
    print "\t-n, --name          Project name"
    print "\t-d, --directory     Project directory"
    print "\t--startFrame        Start frame (float)"
    print "\t--endFrame          End frame (float)"
    print "\t--frameRate         Frames per second (float)"
    print "\t--xRes              X resolution (float)"
    print "\t--yRes              Y resolution (float)"
    print "\t--xPad              Total X padding (float)"
    print "\t--yPad              Total Y padding (float)"
    print "\t--aspectRatio       Pixel aspect ratio (float)"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    ueClient.Client()
    createProject()

    sys.exit(0)

