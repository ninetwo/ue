import sys, os, getopt

import ueClient, ueSpec

import ueCore.AssetUtils as ueAssetUtils

def changeAsset():
    spec = ueSpec.Spec(sys.argv[-1])

    if not spec.proj in ueAssetUtils.getProjectsList():
        print "ERROR: Project does not exist"
        sys.exit(2)

    if not spec.grp in ueAssetUtils.getGroupsList(spec):
        print "ERROR: Group does not exist"
        sys.exit(2)

    if not spec.asst in ueAssetUtils.getAssetsList(spec):
        print "ERROR: Asset does not exist"
        sys.exit(2)

    project = ueAssetUtils.getProject(spec)
    asset = ueAssetUtils.getAsset(spec)

    print "export PROJ=%s; " % spec.proj
    print "export GRP=%s; " % spec.grp
    print "export ASST=%s; " % spec.asst
    print "export PROJ_ROOT=%s; " % project["path"]
    print "export ASST_ROOT=%s" % asset["path"]


def parse():
    sArgs = "h"
    lArgs = ["help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            print "ERROR: Unrecognised argument '%s'" % o
            sys.exit(2)

def usage():
    print "Usage: %s [ASSET SPEC]" % os.path.basename(sys.argv[0])
    print "Sets current ue asset."
    print ""
    print "\t[ASSET SPEC]        ue asset, e.g. proj:grp:asst"
    print "\t                    If you're already uesp'd into an"
    print "\t                    asset, you can also use 'grp:ast' or"
    print "\t                    'asst' if the asset you're uesp'ing"
    print "\t                    into is within the same project/group."
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "ERROR: No asset given"
        sys.exit(2)

    ueClient.Client()

    parse()
    changeAsset()

    sys.exit(1)

