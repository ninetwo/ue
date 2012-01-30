maya_path=/usr/autodesk/maya2012-x64/bin/maya2012

if [[ $PROJ == "" || $GROUP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running maya"
  exit 0
fi

export MAYA_SCRIPT_PATH=$PROJ_ROOT/etc/maya
#export MAYA_SHELF_PATH=$PROJ_ROOT/etc/maya
export PYTHONPATH=$PYTHONPATH

$maya_path $*

