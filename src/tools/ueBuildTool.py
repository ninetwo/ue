#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueEdit
import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate

options = {}
options["assets"] = False
options["print"] = False
options["create"] = False

def main():
    if "spec" not in options:
        print "ERROR: Spec not set"
        sys.exit(2)

    spec = ueSpec.Spec(options["spec"])

    edit = ueEdit.getBuild(spec)

    if options["assets"]:
        if options["print"]:
            for sequence in sorted(edit):
                print "-> %s" % sequence
                for shot in sorted(edit[sequence]):
                    print "---> %s" % shot
        elif options["create"]:
            # Get the group and check agains the data in the edit file to see if anything has changed
            spec = ueSpec.Spec(proj=os.getenv("PROJ"))
            for sequence in sorted(edit):
                print "-> Creating sequence %s ..." % sequence
                spec.grp = sequence
                ueCreate.createGroup(spec, "lib")
                for shot in sorted(edit[sequence]):
                    if shot not in ["black", "white"]:
                        print "---> Creating shot %s ..." % shot
                        spec.asst = shot
                        ueCreate.createAsset(spec, "lib", dbMeta=edit[sequence][shot])


def parse():
    sArgs = "hs:acp"
    lArgs = ["help", "spec=", "assets", "create", "print"]

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
            options["spec"] = a
        elif o in ("-a", "--assets"):
            options["assets"] = True
        elif o in ("-c", "--create"):
            options["create"] = True
        elif o in ("-p", "--print"):
            options["print"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Tool for creating and modifying a ue projects"
    print "build groups and asset libraries based on an edit config."
    print ""
    print "\t-s, --spec          Edit spec"
    print "\t-a, --assets        Asset mode"
    print "\t    -c, --create    Creates assets"
    print "\t    -p, --print     Prints assets"
    print "\t-h, --help          Print this help"

if __name__ == "__main__":
    if os.getenv("PROJ") == None:
        print "Error: uesp before running %s" % os.path.basename(sys.argv[0])
        sys.exit(2)

    parse()
    if not options["assets"]:
        usage()
        sys.exit(0)
    ueClient.Client()
    main()

    sys.exit(0)

