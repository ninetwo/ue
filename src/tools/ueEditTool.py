#!/usr/bin/python

import sys, os, getopt

import ueClient, ueSpec

import ueEdit
import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate

excludedShotNames = ["black", "white"]

options = {}
options["spec"] = "%s:edt:master:master:edit:edt" % os.getenv("PROJ")
options["assets"] = False
options["print"] = False
options["create"] = False
options["play"] = False

def main():
    spec = ueSpec.Spec(options["spec"])

    edit = ueEdit.getEdit(spec)

    if options["assets"]:
        if options["print"]:
            for sequence in edit["sequences"]:
                print "-> %s" % sequence
                for shot in edit[sequence]["shots"]:
                    print "---> %s" % shot
        elif options["create"]:
            # Get the group and check agains the data in the edit file to see if anything has changed
            spec = ueSpec.Spec(proj=os.getenv("PROJ"))
            for sequence in edit["sequences"]:
                print "-> Creating sequence %s ..." % sequence
                spec.grp = sequence
                ueCreate.createGroup(spec, "default")
                for shot in edit[sequence]["shots"]:
                    if shot not in excludedShotNames:
                        print "---> Creating shot %s ..." % shot
                        spec.asst = shot
                        ueCreate.createAsset(spec, "default", dbMeta=edit[sequence][shot])
    elif options["play"]:
        shots = []
        for sequence in edit:
            spec.grp = sequence
            for shot in edit[sequence]:
                spec.asst = shot
                spec.eltype = "storyboard"
                spec.elname = "master"
                spec.elclass = "sb"

                versions = ueAssetUtils.getVersions(spec)

                if len(versions) == 0:
                    print "Nothing"
                    shots.append(os.path.join(os.getenv("UE_PATH"), "lib", "placeholders", "edit.1-24.png"))
                else:
                    print "Something"
                    shots.append(os.path.join(versions[-1]["path"], "edit.1-24.png"))

        arguments = ""
        for path in shots:
            arguments += " %s" % (path)

        print arguments

        os.system("rv %s" % arguments)

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
        elif o in ("-p", "--print", "--play"):
            options["print"] = True
            options["play"] = True
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s -s [SPEC] ..." % os.path.basename(sys.argv[0])
    print "Tool for creating and modifying a ue projects"
    print "sequence groups and assets based on an edit config."
    print ""
    print "\t-s, --spec          Edit spec"
    print "\t                    Defaults to %s" % options["spec"]
    print "\t-a, --assets        Asset mode"
    print "\t    -c, --create    Creates assets"
    print "\t    -p, --print     Prints assets"
    print "\t-p, --play          Play"
    print "\t-h, --help          Print this help"

if __name__ == "__main__":
    if os.getenv("PROJ") == None:
        print "Error: uesp before running %s" % os.path.basename(sys.argv[0])
        sys.exit(2)

    parse()
    if not options["assets"] and not options["play"]:
        usage()
        sys.exit(0)
    ueClient.Client()
    main()

    sys.exit(0)

