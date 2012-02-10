import sys, requests, json

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
        urlargs = self.parseUrlargs(args)

        url = "%s://%s:%i/%s%s.json" % (self.protocol, self.host,
                                        self.port, get, urlargs)

        try:
            request = requests.get(url)
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

        try:
            jsonDict = json.loads(request.text)
        except ValueError:
            jsonDict = {}

        if jsonDict == None:
            jsonDict = {}

        return jsonDict

    def post(self, get, *args, **kwargs):
        urlargs = self.parseUrlargs(args)

        url = "%s://%s:%i/%s%s.json" % (self.protocol, self.host,
                                        self.port, get, urlargs)

        try:
            request = requests.post(url, data=kwargs["data"])
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)

    def put(self, get, spec, **kwargs):
        if not spec.proj == None:
            kwargs["data"]["project"] = spec.proj
        if not spec.grp == None:
            kwargs["data"]["group"] = spec.grp
        if not spec.asst == None:
            kwargs["data"]["asset"] = spec.asst
        if not spec.elclass == None:
            kwargs["data"]["elclass"] = spec.elclass
        if not spec.eltype == None:
            kwargs["data"]["eltype"] = spec.eltype
        if not spec.elname == None:
            kwargs["data"]["elname"] = spec.elname
        if not spec.vers == None:
            kwargs["data"]["version"] = spec.vers

        url = "%s://%s:%i/%s.json" % (self.protocol, self.host,
                                      self.port, get)

        try:
            request = requests.put(url, data=kwargs["data"])
        except IOError, e:
            print "FATAL ERROR: %s" % e
            sys.exit(2)


    def parseUrlargs(self, args):
        if len(args) > 0:
            urlargs = "/"+str("/".join(args))
        else:
            urlargs = ""
        return urlargs


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


    def updateProject(self, spec, data):
        self.put("projects", spec, data=data)

    def updateGroup(self, spec,  data):
        self.put("groups", spec, data=data)

    def updateAsset(self, spec, data):
        self.put("assets", spec, data=data)

    def updateElement(self, spec, data):
        self.put("elements", spec, data=data)

    def updateVersion(self, spec, data):
        self.put("versions", spec, data=data)


    def getConfig(self, *args):
        if len(args) == 1:
            return self.get("config", args[0])
        elif len(args) == 2:
            return self.get("config", args[0], args[1])
        elif len(args) == 3:
            return self.get("config", args[0], args[1], args[2])
        elif len(args) >= 6:
            return self.get("config", args[0], args[1], args[2],
                                      args[3], args[4], args[5])

    def saveConfig(self, spec, data):
        if spec.grp == None:
            self.post("config", spec.proj, data={"config": data})
        elif spec.asst == None:
            self.post("config", spec.proj, spec.grp, data={"config": data})
        elif spec.elclass == None:
            self.post("config", spec.proj, spec.grp, spec.asst,
                      data={"config": data})

