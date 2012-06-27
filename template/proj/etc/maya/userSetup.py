import pymel.core

import ueClient

import ueMaya

ueClient.Client()

pymel.core.scriptJob(event=["NewSceneOpened", ueMaya.ueNewScriptSetup])
#pymel.core.scriptJob(event=["SceneOpened", ueMaya.ueChecker])

