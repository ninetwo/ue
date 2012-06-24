mari_path=/opt/Mari1.4v4/bin/MriBin

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running mari"
  exit 0
fi

$mari_path $*

