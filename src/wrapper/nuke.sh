nuke_path=/usr/local/Nuke6.3v2/Nuke6.3

if [[ $PROJ == "" || $GROUP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running nuke"
  exit 0
fi

export NUKE_PATH=$PROJ_ROOT/etc/nuke

$nuke_path $*

