#!/usr/bin/python

import os

os.system("nuke -t %s" % os.path.join(os.getenv("UE_PATH"), "src/ueTVP/publishCels.py"))

