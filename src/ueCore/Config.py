import json

import ueClient, ueSpec

defaultConfig = {
        "projectDirs": {
               "bin": None,
               "etc": {
                       "nuke": ["template/proj/etc/nuke/*"],
                       "maya": ["template/proj/etc/maya/*"]
                      },
               "seq": None,
               "tmp": None,
               "var": {
                       "thumbs": None
                      }
              },

        "groupDirs": {
              "default": [{
                           },
                            "seq"],
              "lib":     [{
                           },
                           ""]
             },

        "assetDirs": {
             "default": [{
                          "output": None,
                          "render": None,
                          "tmp":    None,
                          "":       ["template/asst/workspace.mel"]
                         },
                         ""],
             "lib":     [{
                          "tmp":     None
                         },
                         ""]
             },

        "assetSettings": {
         "startFrame":  1,
         "endFrame":    96,
         "frameRate":   24,
         "aspectRatio": 1.0,
         "xRes":        1920,
         "yRes":        1080,
         "xPad":        40,
         "yPad":        40
        },

        "assetClasses": {"o":   {
                                 "name": "Output"
                                },
                         "ns":  {
                                 "name": "Nuke script"
                                },
                         "nr":  {
                                 "name": "Nuke render"
                                },
                         "giz": {
                                 "name": "Nuke gizmo"
                                },
                         "scp": {
                                 "name": "Nuke scriptlet"
                                },
                         "ms":  {
                                 "name": "Maya scene"
                                },
                         "mr":  {
                                 "name": "Maya render"
                                },
                         "tvp": {
                                 "name": "TVPaint document"
                                },
                         "cel": {
                                 "name": "Cel sequence"
                                },
                         "ps":  {
                                 "name": "Photoshop document"
                                },
                         "bg":  {
                                 "name": "Background"
                                },
                         "ae":  {
                                 "name": "After Effects document"
                                },
                         "ar":  {
                                 "name": "After Effects render"
                                },
                         "geo": {
                                 "name": "Geometry"
                                },
                         "cam": {
                                 "name": "Camera"
                                },
                         "lgt": {
                                 "name": "Light"
                                },
                         "tex": {
                                 "name": "Texture"
                                }
                        }
}


class Config():
    def __init__(self, spec=ueSpec.Spec()):
#        self.config = ueDefaults.Defaults()
        self.config = defaultConfig

        if not spec.proj == None:
            c = ueClient.client.getConfig(spec.proj)
            if "config" in c:
                self.config = self.mergeConfig(self.config, self.toDict(c["config"]))
        if not spec.grp == None:
            c = ueClient.client.getConfig(spec.proj, spec.grp)
            if "config" in c:
                self.config = self.mergeConfig(self.config, self.toDict(c["config"]))
        if not spec.asst == None:
            c = ueClient.client.getConfig(spec.proj, spec.grp, spec.asst)
            if "config" in c:
                self.config = self.mergeConfig(self.config, self.toDict(c["config"]))

    def toDict(self, s):
        return json.loads(s.replace("'", '"').replace("None", "null"))

    def mergeConfig(self, slave, master):
        config = dict(slave.items()+master.items())

        for c in config:
            if type(config[c]).__name__ == "dict":
                if c in slave and c in master:
                    config[c] = self.mergeConfig(slave[c], master[c])

        return config

