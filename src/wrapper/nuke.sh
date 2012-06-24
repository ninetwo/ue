nuke_path=/usr/local/Nuke6.3v3/Nuke6.3

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running nuke"
  exit 0
fi

export NUKE_PATH=$PROJ_ROOT/etc/nuke:/opt/Bokeh-Nuke6.3-1.2.5-Linux:/opt/atomkraft-1.1.4-0/plugin:/usr/OFX/Plugins/Trapcode
export PYTHONPATH=$PYTHONPATH:$PROJ_ROOT/etc/nuke:$UE_PATH/tools/nuke

$nuke_path --nukex $*

