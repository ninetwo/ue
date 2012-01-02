#!/usr/bin/python

import sys, os
import getopt, json

import ueCore.Settings as ueSettings
import ueCore.AssetUtils as ueAssetUtils
import ueCore.ConfigUtils as ueConfigUtils
import ueCore.FileUtils as ueFileUtils

global asset

def createAsset():
    if "name" not in asset:
        print "ERROR: Asset name not set"
        sys.exit(2)

    if "group" not in asset:
        print "ERROR: Group not set"
        sys.exit(2)

    if "directory" not in asset:
        print "ERROR: Asset directory not set"
        sys.exit(2)

    config = ueConfigUtils.getConfig(os.getenv("PROJ"), asset["group"])
    groups = ueAssetUtils.getGroups(os.getenv("PROJ"))

    if asset["group"] not in groups:
        print "ERROR: Group '%s' does not exist" % asset["group"]

    if not asset["type"] in config["ASSET_DIRS"]:
        print "ERROR: Asset type '%s' does not exist" % asset["type"]
        sys.exit(2)

    assets = ueAssetUtils.getAssets(os.getenv("PROJ"), asset["group"])

    if asset["name"] in assets:
        print "ERROR: Asset '%s' already exists" % asset["name"]
        sys.exit(2)

    rootPath = os.path.join(groups[asset["group"]]["path"], config["ASSET_DIRS"][asset["type"]][1])
    d = os.path.join(rootPath, asset["name"])

    ueFileUtils.createDirTree(d, config["ASSET_DIRS"][asset["type"]][0])

    if not asset["config"] == {}:
        ueConfigUtils.saveConfig(asset["config"], d)

    assets[asset["name"]] = {"path": d, "type": asset["type"]}
    p = os.path.join(groups[asset["group"]]["path"], "etc", "assets")
    try:
        print "Adding asset to group asset list '%s'" % p
        f = open(p, "w")
        f.write(json.dumps(assets, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Adding asset to group asset list '%s' (%s)" % (p, e)


def parse():
    sArgs = "hn:t:g:d:s:e:"
    lArgs = ["help", "name=", "type=", "group=", "directory=", "startframe=", "endframe="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], sArgs, lArgs)
    except getopt.GetoptError, e:
        print "ERROR: Parsing argument (%s)" % e
        sys.exit(2)

    asset["type"] = "default"
    asset["directory"] = os.getenv("PROJ_ROOT")
    asset["config"] = {}

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-n", "--name"):
            asset["name"] = a
        elif o in ("-t", "--type"):
            asset["type"] = a
        elif o in ("-g", "--group"):
            asset["group"] = a
        elif o in ("-d", "--directory"):
            asset["directory"] = a
        elif o in ("-s", "--startframe"):
            if not "ENVS" in asset["config"]:
                asset["config"]["ENVS"] = {}
            asset["config"]["ENVS"]["STARTFRAME"] = a
        elif o in ("-e", "--endframe"):
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
    print "\t-g, --group         Group that the asset will be created in"
    print "\t-d, --directory     Asset directory"
    print "\t                    Will use group or project default if not set"
    print "\t-s, --startframe    Start frame"
    print "\t-e, --endframe      End frame"
    print "\t-h, --help          Print this help"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    if not "PROJ" in os.environ:
        print "ERROR: No project set"
        sys.exit(2)

    asset = {}

    parse()
    createAsset()

    sys.exit(0)

