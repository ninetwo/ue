import os, json

def getConfig(*args):
    import ueCore.AssetUtils as ueAssetUtils

    config = loadConfig(os.getenv("UE_PATH"))

    if len(args) > 0:
        project = ueAssetUtils.getProject(args[0])
        if not project == None:
            config = mergeConfig(config, loadConfig(project["path"]))
    if len(args) > 1:
        group = ueAssetUtils.getGroup(args[0], args[1])
        if not group == None:
            config = mergeConfig(config, loadConfig(group["path"]))
    if len(args) > 2:
        asset = ueAssetUtils.getAsset(args[0], args[1], args[2])
        if not asset == None:
            config = mergeConfig(config, loadConfig(asset["path"]))

    return config

def mergeConfig(slave, master):
    config = dict(slave.items()+master.items())
    for c in config:
        if type(config[c]).__name__ == "dict":
            if c in slave and c in master:
                config[c] = mergeConfig(slave[c], master[c])
    return config

def loadConfig(path):
    configFile = os.path.join(path, "etc", "config")
    config = {}
    if os.path.exists(configFile):
        try:
            #print "Loading config file '%s'" % configFile
            f = open(configFile, "r")
            config = json.loads(f.read())
            f.close()
        except IOError, e:
            print "Error: Loading config file '%s' (%s)" % (path, e)
    return config

def saveConfig(config, path):
    configFile = os.path.join(path, "etc", "config")
    try:
        #print "Writing config file '%s'" % configFile
        f = open(configFile, "w")
        f.write(json.dumps(config, sort_keys=True, indent=4))
        f.close()
    except IOError, e:
        print "Error: Saving config file '%s' (%s)" % (path, e)

