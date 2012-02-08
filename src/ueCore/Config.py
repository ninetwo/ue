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
                            "etc": None
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
                          "name": "Output",
                          "desc": "Final asset output"
                         },
                  "tvp": {
                          "name": "TVPaint",
                          "desc": "TVPaint document"
                         },
                  "cel": {
                          "name": "Cel",
                          "desc": "Cel image sequence",
                          "pathprepend": "cel",
                          "pathappend":  "%%version%%"
                         },
                  "bg":  {
                          "name": "Background",
                          "desc": "Background image"
                         },
                  "c":   {
                          "name": "Comp script",
                          "desc": "Comp script"
                         },
                  "s":   {
                          "name": "3D scene",
                          "desc": "3D scene"
                         },
                  "cp":  {
                          "name": "Comp render",
                          "desc": "Render from comp script",
                          "pathprepend": "render",
                          "pathappend":  "%%version%%"
                         },
                  "rn":  {
                          "name": "3D render",
                          "desc": "Render from 3D",
                          "pathprepend": "render",
                          "pathappend":  "%%version%%"
                         },
                  "giz": {
                          "name": "Nuke Gizmo",
                          "desc": "Nuke Gizmo",
                          "pathprepend": "gizmo"
                         },
                  "ani": {
                          "name": "Animatic footage",
                          "desc": "Animatic footage"
                         },
                  "geo": {
                          "name": "Geometry",
                          "desc": "Geometry"
                         },
                  "cam": {
                          "name": "Camera",
                          "desc": "Camera"
                         },
                  "lgt": {
                          "name": "Light",
                          "desc": "Light"
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

