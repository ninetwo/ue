import sys, json

import ueClient, ueSpec

import ueRender.Job as ueRenderJob

ueClient.Client()

sourceSpec = ueSpec.Spec(sys.argv[1])
destSpec = ueSpec.Spec(sys.argv[2])
options = json.loads(sys.argv[6])

job = ueRenderJob.Job(sourceSpec, destSpec, sys.argv[3],
                      frame_start=int(sys.argv[4]),
                      frame_end=int(sys.argv[5]), writeNode=options["writeNode"])

job.createScript()
job.spool()

