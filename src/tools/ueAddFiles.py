#!/usr/bin/python

import sys, os, shutil
import glob, getopt

import ueCore.AssetUtils as ueAssetUtils
import ueCore.CreateUtils as ueCreateUtils

global config

def addFiles():
#    if not "files" in config:
#        print "ERROR: No files given"
#        sys.exit(2)

#    if not "element" in config:
#        print "ERROR: No element given"
#        sys.exit(2)

    e = sys.argv[1].split(":")

    if not len(e) == 6:
        print "ERROR: Incomplete element"
        sys.exit(2)

    proj = e[0]
    grp = e[1]
    asst = e[2]
    elclass = e[5]
    eltype = e[4]
    name = e[3]

    files = sys.argv[2:]

    d = ueAssetUtils.getElement(proj, grp, asst, elclass, eltype, name)
    if d == None:
        d = ueCreateUtils.createElement(proj, grp, asst, elclass, eltype, name)

    vers = ueAssetUtils.getVersions(proj, grp, asst, elclass, eltype, name)
    fName = ueCreateUtils.getElementName(proj, grp, asst, elclass, eltype, name, len(vers)+1)
    ext = files[0].split(".")[-1]

    p = ueCreateUtils.createVersion(proj, grp, asst, elclass, eltype, name, len(vers)+1,
                                    source=files[0])

    if len(files) == 1:
        fPath = os.path.join(p["path"], "%s.%s" % (fName, ext))
        shutil.copy(files[0], fPath)
    else:
        for f in files:
            fPath = os.path.join(p["path"], "%s.%04d.%s" % (fName, files.index(f)+1, ext))
            shutil.copy(f, fPath)

def parse():
    global config

    sArgs = "h"
    lArgs = ["help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    config = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)


def usage():
    print "Usage: %s [ELEMENT NAME] [FILES]" % os.path.basename(sys.argv[0])
    print "Adds files to a ue element."
    print ""
    print "\t[ELEMENT NAME]      ue element name, e.g."
    print "\t                    proj:grp:asst:name:type:class"
    print "\t[FILES]             Path to file(s). Can include"
    print "\t                    wildcards."
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    parse()
    addFiles()

    sys.exit(0)

