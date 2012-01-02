import sys, os
import getopt, json

import ueCore.ConfigUtils as ueConfigUtils
import ueCore.AssetUtils as ueAssetUtils

def changeAsset():
    tmp = sys.argv[-1].split(":")

    if len(tmp) == 1 and not "PROJ" in os.environ:
        proj = tmp[0]

        project = ueAssetUtils.getProject(proj)

        if project == None:
            print "ERROR: Project does not exist"
            sys.exit(2)

        config = ueConfigUtils.getConfig(proj)

        print "export PROJ=%s; " % proj
        print "export PROJ_ROOT=%s; " % project["path"]
        print "export ASST_ROOT=%s; " % project["path"]
        for p in config["ENVS"]:
            print "export %s=%s; " % (p, config["ENVS"][p])

        sys.exit(0)

    if len(tmp) == 3:
        proj = tmp[0]
        group = tmp[1]
        asset = tmp[2]
    elif len(tmp) == 2:
        if not "PROJ" in os.environ:
            print "ERROR: No project specified"
            sys.exit(2)
        proj = os.getenv("PROJ")
        group = tmp[0]
        asset = tmp[1]
    elif len(tmp) == 1:
        if not "PROJ" in os.environ:
            print "ERROR: No project specified"
            sys.exit(2)
        if not "GROUP" in os.environ:
            print "ERROR: No group specified"
            sys.exit(2)
        proj = os.getenv("PROJ")
        group = os.getenv("GROUP")
        asset = tmp[0]
    else:
        print "ERROR: Invalid asset"
        sys.exit(2)

    if not proj in ueAssetUtils.getProjectsList():
        print "ERROR: Project does not exist"
        sys.exit(2)

    if not group in ueAssetUtils.getGroupsList(proj):
        print "ERROR: Group does not exist"
        sys.exit(2)

    assets = ueAssetUtils.getAsset(proj, group, asset)

    if assets == None:
        print "ERROR: Asset does not exist"
        sys.exit(2)

    config = ueConfigUtils.getConfig(proj, group, asset)

    print "export PROJ=%s; export GROUP=%s; export ASST=%s; " % (proj, group, asset)
    print "export PROJ_ROOT=%s; " % ueAssetUtils.getProject(proj)["path"]
    print "export ASST_ROOT=%s; " % assets["path"]
    for p in config["ENVS"]:
        print "export %s=%s; " % (p, config["ENVS"][p])


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
    print "Usage: %s [ASSET]" % os.path.basename(sys.argv[0])
    print "Sets current ue asset."
    print ""
    print "\t[ASSET]             ue asset, e.g. proj:grp:asst"
    print "\t                    If you're already uesp'd into an"
    print "\t                    asset, you can also use 'grp:ast' or"
    print "\t                    'asst' if the asset you're uesp'ing"
    print "\t                    into is within the same project/group."
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "ERROR: No asset given"
        sys.exit(2)

    parse()
    changeAsset()

    sys.exit(1)

