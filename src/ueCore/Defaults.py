class Defaults():
    def __init__(self):
        self.projectDirs = {
               "bin": None,
               "etc": {
                       "nuke": ["template/proj/etc/nuke/*"],
                       "maya": ["template/proj/etc/maya/*"]
                      },
               "seq": None,
               "tmp": None
              }

        self.groupDirs =  {
              "default": [{
                           },
                            "seq"],
              "lib":     [{
                            "etc": None
                           },
                           ""]
             }

        self.assetDirs = {
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
             }

        self.assetSettings = {
         "STARTFRAME":  1,
         "ENDFRAME":    96,
         "FRAMERATE":   24,
         "ASPECTRATIO": 1.0,
         "XRES":        1920,
         "YRES":        1080,
         "XPAD":        40,
         "YPAD":        40
        }

        self.assetClasses = {"o":   {
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

