import sys, urllib, json

import ueSpec

global client

class Client():
    def __init__(self):
        global client

        self.protocol = "http"
        self.host = "localhost"
        self.port = 3000

        client = self

    def get(self, get, *args):
        if len(args) > 0:
            urlargs = "/"+str("/".join(args))
        else:
            urlargs = ""

        url = "%s://%s:%i/%s%s.json" % (self.protocol, self.host,
                                        self.port, get, urlargs)

        try:
            data = urllib.urlopen(url)
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

        try:
            jsonDict = json.load(data)
        except ValueError:
            jsonDict = {}

        if jsonDict == None:
            jsonDict = {}

        return jsonDict

    def post(self, get, *args, **kwargs):
        if len(args) > 0:
            urlargs = "/"+str("/".join(args))
        else:
            urlargs = ""

        url = "%s://%s:%i/%s%s.json" % (self.protocol, self.host,
                                        self.port, get, urlargs)

        try:
            urllib.urlopen(url, urllib.urlencode(kwargs["data"]))
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

    def getConfig(self, *args):
        if len(args) == 1:
            return self.get("config", args[0])
        elif len(args) == 2:
            return self.get("config", args[0], args[1])
        elif len(args) == 3:
            return self.get("config", args[0], args[1], args[2])

    def getProjects(self):
        return self.get("projects")

    def getProject(self, spec):
        return self.get("projects", spec.proj)

    def getGroups(self, spec):
        return self.get("groups", spec.proj)

    def getGroup(self, spec):
        return self.get("groups", spec.proj, spec.grp)

    def getAssets(self, spec):
        return self.get("assets", spec.proj, spec.grp)

    def getAsset(self, spec):
        return self.get("assets", spec.proj, spec.grp, spec.asst)

    def getElements(self, spec):
        return self.get("elements", spec.proj, spec.grp, spec.asst)

    def getElement(self, spec):
        return self.get("elements", spec.proj, spec.grp, spec.asst,
                        spec.elclass, spec.eltype, spec.elname)

    def saveConfig(self, spec, data):
        if spec.grp == None:
            self.post("config", spec.proj, data={"config": data})
        elif spec.asst == None:
            self.post("config", spec.proj, spec.grp, data={"config": data})
        elif spec.elclass == None:
            self.post("config", spec.proj, spec.grp, spec.asst,
                      data={"config": data})

    def saveProject(self, spec, data):
        self.post("projects", data=data)

    def saveGroup(self, spec, data):
        self.post("groups", spec.proj, data=data)

    def saveAsset(self, spec, data):
        self.post("assets", spec.proj, spec.grp, data=data)

    def saveElement(self, spec, data):
        self.post("elements", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname, data=data)

    def saveVersion(self, spec, data):
        self.post("versions", spec.proj, spec.grp, spec.asst,
                  spec.elclass, spec.eltype, spec.elname, data=data)

