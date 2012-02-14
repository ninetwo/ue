import os, sys, json

job = {}

frameNum = os.getenv("DRQUEUE_FRAME")

f = open(sys.argv[1], "r")
job = json.loads(f.read())
f.close()

if not str(frameNum) in job:
    print "ERROR: Frame %i not found" % frameNum
    sys.exit(2)

frame = job[str(frameNum)]

os.environ["PROJ"] = frame["proj"]
os.environ["GRP"] = frame["grp"]
os.environ["ASST"] = frame["asst"]
os.environ["PROJ_ROOT"] = frame["proj_root"]
os.environ["ASST_ROOT"] = frame["asst_root"]

os.system(frame["cmd"])

