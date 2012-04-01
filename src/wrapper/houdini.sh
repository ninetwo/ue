houdini_path=/opt/hfs12.0.543.9
houdini_bin=/opt/hfs12.0.543.9/bin/houdini

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running houdini"
  exit 0
fi

cd $houdni_path
source houdini_setup
cd

$houdini_bin $*

