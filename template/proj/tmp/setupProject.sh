#!/bin/bash

proj=$1

ueCreateGroup -s $proj -n libDev -t lib
ueCreateAsset -s $proj:libDev -n global -t lib
ueCreateAsset -s $proj:libDev -n rnd

ueCreateGroup -s $proj -n libSets -t lib
ueCreateAsset -s $proj:libSets -n global -t lib

ueCreateGroup -s $proj -n libVehicles -t lib
ueCreateAsset -s $proj:libVehicles -n global -t lib

ueCreateGroup -s $proj -n libProps -t lib
ueCreateAsset -s $proj:libProps -n global -t lib

ueCreateGroup -s $proj -n libAnim -t lib
ueCreateAsset -s $proj:libAnim -n global -t lib

ueCreateGroup -s $proj -n edt -t edt
ueCreateAsset -s $proj:edt -n master -t edt

ueCreateGroup -s $proj -n dev
ueCreateAsset -s $proj:dev -n global -t lib
ueCreateAsset -s $proj:dev -n rnd

#ueAddFiles -s $proj:lib:global:ueRead:fileUtils:giz -f $UE_PATH/lib/gizmos/ueRead.gizmo
#ueAddFiles -s $proj:lib:global:ueWrite:fileUtils:giz -f $UE_PATH/lib/gizmos/ueWrite.gizmo

#ueAddFiles -s $proj:lib:global:tvpReformat:celUtils:giz -f $UE_PATH/../ueScripts/tvpReformat.gizmo
#ueAddFiles -s $proj:lib:global:reColour:celUtils:giz -f $UE_PATH/../ueScripts/reColour.gizmo

#cp $UE_PATH/../ueScripts/tvp2cel.* $UE_PATH/../ueScripts/edl2assets.py $PROJ_ROOT/bin/

