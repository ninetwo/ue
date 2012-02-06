#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueCore.Create as ueCreate

asset = {}

def createAsset():
    if "name" not in asset:
        print "ERROR: Asset name not set"
        sys.exit(2)

    if "directory" not in asset:
        print "ERROR: Asset directory not set"
        sys.exit(2)

    spec = ueSpec.Spec(asset["spec"]+":"+asset["name"])

    ueCreate.createAsset(spec, asset["type"])

def parse():
    sArgs = "hn:s:t:d:"
    lArgs = ["help", "name=", "spec=", "type=", "directory=", "startframe=", "endframe="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    asset["spec"] = ueSpec.Spec(os.getenv("PROJ"), os.getenv("GRP"))
    asset["type"] = "default"
    asset["directory"] = os.getenv("PROJ_ROOT")
    asset["config"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            asset["name"] = a
        elif o in ("-s", "--spec"):
            asset["spec"] = a
        elif o in ("-t", "--type"):
            asset["type"] = a
        elif o in ("-d", "--directory"):
            asset["directory"] = a
        elif o in ("--startframe"):
            if not "ENVS" in asset["config"]:
                asset["config"]["ENVS"] = {}
            asset["config"]["ENVS"]["STARTFRAME"] = a
        elif o in ("--endframe"):
            if not "ENVS" in asset["config"]:
                asset["config"]["ENVS"] = {}
            asset["config"]["ENVS"]["ENDFRAME"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s -n [NAME] -g [GROUP] ..." % os.path.basename(sys.argv[0])
    print "Creates a new ue asset."
    print ""
    print "\t-n, --name          Asset name"
    print "\t-s, --spec          "
    print "\t-d, --directory     Asset directory"
    print "\t                    Will use group or project default if not set"
    print "\t--startframe        Start frame"
    print "\t--endframe          End frame"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    ueClient.Client()

    parse()
    createAsset()

    sys.exit(0)

