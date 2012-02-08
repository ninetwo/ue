hiero_path=/opt/Hiero1.0v1b3/bin/Hiero1.0v1b3

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running hiero"
  exit 0
fi

$hiero_path $*

