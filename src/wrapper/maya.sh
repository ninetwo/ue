maya_path=/usr/autodesk/maya2011-x64/bin/maya2011

if [[ $PROJ == "" || $GROUP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running maya"
  exit 0
fi

$maya_path $*

