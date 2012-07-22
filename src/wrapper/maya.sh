maya_path=/usr/autodesk/maya2012-x64/bin/maya2012

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running maya"
  exit 0
fi

export MAYA_SCRIPT_PATH=$MAYA_SCRIPT_PATH:$PROJ_ROOT/etc/maya
export MAYA_PLUG_IN_PATH=$MAYA_PLUG_IN_PATH:$UE_PATH/src/ueMaya/nodes
#export MAYA_SHELF_PATH=$PROJ_ROOT/etc/maya
export PYTHONPATH=$PYTHONPATH:$PROJ_ROOT/etc/maya:$UE_PATH/tools/maya

$maya_path $*

