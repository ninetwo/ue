tvp_path=/usr/bin/tvp-animation-9-pro

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running nuke"
  exit 0
fi

$tvp_path $*
#"script=$UE_PATH/src/ueTVP/Startup.grg" $*

