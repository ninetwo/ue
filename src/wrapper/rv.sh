rv_path=/opt/rv-Linux-x86-64-3.12.14/bin/rv.bin

if [[ $PROJ == "" || $GRP == "" || $ASST == "" ]]; then
  echo "Error: uesp before running rv"
  exit 0
fi

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rv-Linux-x86-64-3.12.14/libWorking

$rv_path $*

