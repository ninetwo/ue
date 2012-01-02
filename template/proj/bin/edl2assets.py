#!/usr/bin/python

import sys, os
import getopt, re

global config

fps = 24

def parseEdl():
    if not os.path.exists(sys.argv[-1]):
        print "ERROR: File '%s' not found" % sys.argv[-1]
        sys.exit(2)

    f = open(sys.argv[-1])

    l = f.readline()
    while l:
        i = l.split()

        if i[0] == "TITLE:":
            t = re.sub("PART", "Part", i[1])
            print "Group: %s" % t
            if config["create"]:
                print "Create group"
        elif re.match("[{3}0-9]", i[0]):
            s = i[4].split(":")
            e = i[5].split(":")
            start = 1
            end = int(e[-1])+\
                  (int(e[-2])*config["fps"])+\
                  (int(e[-3])*60*config["fps"])+\
                  ((int(e[-4])-1)*60*60*config["fps"])
            print "Asset: %s %i - %i" % (i[1], start, end)
            if config["create"]:
                print "Create asset"

        l = f.readline()

def parseArgs():
    global config

    sArgs = "hdf:"
    lArgs = ["help", "dry-run", "frame-rate="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    config = {}
    config["create"] = True
    config["fps"] = fps

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-d", "--dry-run"):
            config["create"] = False
        elif o in ("-f", "--frame-rate"):
            config["fps"] = int(a)
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s [...] EDL_FILE" % os.path.basename(sys.argv[0])
    print "Creates ue group and assets from EDL file."
    print ""
    print "\t-d, --dry-run       Don't create any assets, just print"
    print "\t                    what would be created"
    print "\t-f, --frame-rate    FPS, used to calculate frame range"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "ERROR: No EDL file given"
        sys.exit(2)

    parseArgs()
    parseEdl()

    sys.exit(0)

