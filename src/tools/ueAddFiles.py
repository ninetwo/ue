#!/usr/bin/python

import sys, os
import glob, getopt

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils
import ueCore.Create as ueCreate
import ueCore.FileUtils as ueFileUtils

config = {}

def addFiles():
    if not "files" in config:
        print "ERROR: No files given"
        sys.exit(2)

    if not "spec" in config:
        print "ERROR: No element spec given"
        sys.exit(2)

    d = ueAssetUtils.getElement(config["spec"])
    if d == {}:
        d = ueCreate.createElement(config["spec"])

    p = ueCreate.createVersion(config["spec"])

    config["spec"].vers = p["version"]

    files = glob.glob(config["files"])

    path = p["path"]
    name = ueAssetUtils.getElementName(config["spec"])
    ext = files[0].split(".")[-1]

    if len(files) == 1:
        dest = os.path.join(path, "%s.%s" % (name, ext))
        ueFileUtils.copyFile(files[0], dest)
    else:
        for f in sorted(files):
            dest = os.path.join(path, "%s.%04d.%s" % (name, files.index(f)+1, ext))
            ueFileUtils.copyFile(f, dest)


def parse():
    sArgs = "hs:f:"
    lArgs = ["help", "spec=", "files="]

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
            config["spec"] = ueSpec.Spec(a)
        elif o in ("-f", "--files"):
            config["files"] = a
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s -s [ELEMENT] -f [FILES]" % os.path.basename(sys.argv[0])
    print "Adds files to a ue element."
    print ""
    print "\t-s, --spec          ue element name, e.g."
    print "\t                    proj:grp:asst:name:type:class"
    print "\t-f, --files         Path to file(s). Can include"
    print "\t                    wildcards."
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    ueClient.Client()

    parse()
    addFiles()

    sys.exit(0)

